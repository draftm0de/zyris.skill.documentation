#!/usr/bin/env python3
"""Immutable local release preparation and catalog promotion. No implicit publication."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import zipfile
sys.dont_write_bytecode = True
import plugin


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(['git', '-C', str(plugin.ROOT), *args], text=True).strip()


def snapshot(path):
    if path.is_symlink():
        raise ValueError('Symlink output forbidden')
    result = {}
    for p in path.rglob('*'):
        if p.is_symlink():
            raise ValueError('Symlink output forbidden')
        if p.is_file():
            result[p.relative_to(path).as_posix()] = p.read_bytes()
    return result


def commit_directory(staged, output):
    """Exclusive lock, atomic first write, identical retry only; never overwrite."""
    output = Path(output).absolute()
    output.parent.mkdir(parents=True, exist_ok=True)
    lock = output.with_name(output.name + '.lock')
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.close(fd)
        if output.exists() or output.is_symlink():
            if snapshot(output) != snapshot(staged):
                raise ValueError('Immutable output conflict; choose a new version/output')
            return
        os.rename(staged, output)
    finally:
        lock.unlink()


def prepare(tag, output, preview=False):
    manifest = plugin.configuration()[0]
    version = tag.removeprefix('v')
    if tag != 'v' + version:
        raise ValueError('Tag must start with v')
    version, portable, claude = plugin.payload(version)
    commit = git('rev-parse', 'HEAD')
    dirty = bool(git('status', '--porcelain', '--untracked-files=all'))
    if not preview:
        if dirty:
            raise ValueError('Release requires a clean checkout')
        if git('rev-parse', tag + '^{commit}') != commit:
            raise ValueError('Tag does not identify HEAD')
    changelog = plugin.ROOT / 'CHANGELOG.md'
    if not changelog.is_file():
        raise ValueError('Missing CHANGELOG.md')
    match = plugin.re.search(r'^## \[' + plugin.re.escape(version) + r'\][^\n]*\n(.*?)(?=^## |\Z)', changelog.read_text(), plugin.re.MULTILINE | plugin.re.DOTALL)
    if not match or not match.group(1).strip():
        raise ValueError('Missing nonempty CHANGELOG.md section for ' + version)
    notes = ('# ' + manifest['name'] + ' ' + version + '\n\n' + match.group(1).strip() + '\n').encode()
    output = Path(output).absolute()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.release-', dir=output.parent) as temporary:
        stage = Path(temporary) / 'bundle'; stage.mkdir()
        for host, files in (('claude', claude), ('codex', plugin.codex_payload(portable)), ('chatgpt', portable)):
            plugin.archive(stage / f'{manifest["name"]}-{version}-{host}.zip', files)
        (stage / 'release-notes.md').write_bytes(notes)
        assets = {name: digest(data) for name, data in snapshot(stage).items()}
        # Payload digest identifies dirty previews without pretending they are committed releases.
        record = {'schema_version': 1, 'name': manifest['name'], 'version': version,
                  'tag': tag, 'commit': commit, 'repository': manifest.get('repository'),
                  'preview': preview, 'dirty': dirty, 'assets': assets}
        (stage / 'release.json').write_bytes(encode(record))
        sums = {name: digest(data) for name, data in snapshot(stage).items()}
        (stage / 'SHA256SUMS').write_text(''.join(f'{value}  {name}\n' for name, value in sorted(sums.items())))
        commit_directory(stage, output)
    return record


def verify_bundle(bundle, allow_preview=False):
    files = snapshot(Path(bundle))
    record = json.loads(files['release.json'])
    name, version = record.get('name'), record.get('version')
    if (not isinstance(name, str) or not plugin.re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name)
            or not isinstance(version, str) or not plugin.re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-(?:alpha|beta|rc)\.(?:0|[1-9]\d*))?', version)
            or record.get('tag') != 'v' + version
            or not plugin.re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', str(record.get('commit', '')))
            or type(record.get('preview')) is not bool or type(record.get('dirty')) is not bool
            or (not record['preview'] and record['dirty'])):
        raise ValueError('Invalid release provenance')
    required = {f'{name}-{version}-{host}.zip' for host in ('claude', 'codex', 'chatgpt')} | {'release-notes.md'}
    if set(record.get('assets', {})) != required:
        raise ValueError('Invalid release asset inventory')
    if record['preview'] and not allow_preview:
        raise ValueError('Preview cannot be promoted/published')
    expected = ''.join(f'{digest(data)}  {name}\n' for name, data in sorted(files.items()) if name != 'SHA256SUMS')
    if files['SHA256SUMS'].decode() != expected:
        raise ValueError('Checksum mismatch')
    if set(record['assets']) != set(files) - {'release.json', 'SHA256SUMS'}:
        raise ValueError('Unexpected bundle assets')
    for asset_name, checksum in record['assets'].items():
        if digest(files[asset_name]) != checksum:
            raise ValueError('Asset checksum mismatch')
    for host, manifest_path in (('claude', '.claude-plugin/plugin.json'), ('codex', '.codex-plugin/plugin.json'), ('chatgpt', 'plugin.json')):
        with zipfile.ZipFile(Path(bundle) / f'{name}-{version}-{host}.zip') as archive:
            manifest = json.loads(archive.read(manifest_path))
            if manifest['name'] != name or manifest['version'] != version:
                raise ValueError('Artifact/manifest conflict')
    return record


def catalog(bundles, output, allow_preview=False):
    """Generate a complete desired catalog snapshot, suitable for a reviewed catalog PR."""
    output = Path(output).absolute(); output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.catalog-', dir=output.parent) as temporary:
        stage = Path(temporary) / 'catalog'; stage.mkdir()
        claude_entries, codex_entries, provenance = [], [], []
        seen = set()
        for bundle in sorted(map(Path, bundles)):
            record = verify_bundle(bundle, allow_preview)
            name, version = record['name'], record['version']
            if name in seen or not plugin.re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
                raise ValueError('Invalid/duplicate plugin identity')
            seen.add(name)
            merged = {}
            for host, manifest_path in [('claude', '.claude-plugin/plugin.json'), ('codex', '.codex-plugin/plugin.json')]:
                with zipfile.ZipFile(bundle / f'{name}-{version}-{host}.zip') as archive:
                    for info in archive.infolist():
                        relative = PurePosixPath(info.filename)
                        if relative.is_absolute() or '..' in relative.parts or '\\' in info.filename or info.filename in ('', '.') or (info.external_attr >> 16) & 0o170000 == 0o120000:
                            raise ValueError('Unsafe archive member')
                        data = archive.read(info)
                        if info.filename in merged and merged[info.filename] != data:
                            raise ValueError('Host payload conflict')
                        merged[info.filename] = data
                metadata = json.loads(merged[manifest_path])
                if metadata['name'] != name or metadata['version'] != version:
                    raise ValueError('Artifact/manifest conflict')
            for relative, data in merged.items():
                path = stage / 'plugins' / name / relative
                path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
            claude_entries.append({'name': name, 'version': version, 'description': metadata['description'], 'source': './plugins/' + name})
            codex_entries.append({'name': name, 'source': {'source': 'local', 'path': './plugins/' + name}, 'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}})
            provenance.append(record)
        for relative, data in [('.claude-plugin/marketplace.json', {'name': 'zyris', 'owner': {'name': 'ZYRIS'}, 'plugins': claude_entries}), ('.agents/plugins/marketplace.json', {'name': 'zyris', 'interface': {'displayName': 'ZYRIS'}, 'plugins': codex_entries}), ('provenance.json', provenance)]:
            path = stage / relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(encode(data))
        (stage / 'README.md').write_text('# ZYRIS generated catalog\n\nGenerated from verified release bundles. Do not edit plugin files manually.\n' + ('\nLOCAL TEST PREVIEW — not published or approved for end users.\n' if allow_preview else ''))
        commit_directory(stage, output)
    return {'plugins': sorted(seen), 'preview': allow_preview}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('prepare'); p.add_argument('--tag', required=True); p.add_argument('--output', required=True); p.add_argument('--preview', action='store_true')
    p = sub.add_parser('catalog'); p.add_argument('--bundle', action='append', required=True); p.add_argument('--output', required=True); p.add_argument('--allow-preview', action='store_true')
    p = sub.add_parser('verify'); p.add_argument('bundle'); p.add_argument('--allow-preview', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'prepare': result = prepare(args.tag, args.output, args.preview)
        elif args.command == 'catalog': result = catalog(args.bundle, args.output, args.allow_preview)
        else: result = verify_bundle(args.bundle, args.allow_preview)
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError, zipfile.BadZipFile) as error:
        parser.exit(1, str(error) + '\n')

if __name__ == '__main__': main()
