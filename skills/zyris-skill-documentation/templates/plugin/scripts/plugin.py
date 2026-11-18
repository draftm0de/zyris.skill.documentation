#!/usr/bin/env python3
"""Build and manage local plugin distributions. Never publish or upload implicitly."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MARKER = '.zyris-generated'
CONFIG_KEY = 'io.zyris.distribution'


def read_file(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f'Expected a regular source file: {path}')
    return path.read_bytes()


def source_path(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or '..' in Path(relative).parts:
        raise ValueError('Source paths must be repository-relative')
    path = root
    for part in Path(relative).parts:
        path /= part
        if path.is_symlink():
            raise ValueError(f'Symlink in source: {relative}')
    return path


def configuration(root=None):
    root = Path(root) if root is not None else ROOT
    manifest = json.loads(read_file(root / 'plugin.json'))
    if not isinstance(manifest, dict):
        raise ValueError('plugin.json must be an object')
    name = manifest.get('name')
    if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('Plugin name must be lowercase kebab-case')
    version = manifest.get('version', '')
    if not isinstance(version, str) or not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', version):
        raise ValueError('plugin.json version must be a numeric major.minor.patch base version')
    if not isinstance(manifest.get('description'), str) or not manifest['description']:
        raise ValueError('Plugin description is required')
    if not isinstance(manifest.get('extensions', {}), dict):
        raise ValueError('extensions must be an object')
    config = manifest.get('extensions', {}).get(CONFIG_KEY, {})
    if not isinstance(config, dict) or set(config) - {'skillRoot', 'marketplace', 'files'}:
        raise ValueError('Unsupported distribution configuration')
    skill_root = config.get('skillRoot', 'skills')
    source = source_path(root, skill_root)
    if not source.is_dir() or not list(source.glob('*/SKILL.md')):
        raise ValueError('skillRoot must contain canonical skill folders')
    market = config.get('marketplace', name + '-local')
    if not isinstance(market, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', market):
        raise ValueError('Invalid marketplace name')
    extra = config.get('files', {})
    if not isinstance(extra, dict):
        raise ValueError('Distribution files must map destination paths to source paths')
    for destination, origin in extra.items():
        if (not isinstance(destination, str) or not destination or Path(destination).is_absolute()
                or any(part in ('.', '..') or part.startswith('.') for part in destination.split('/'))
                or destination == 'plugin.json'):
            raise ValueError('Unsafe or reserved distribution destination')
        if isinstance(origin, str) and (any(part.startswith('.env') for part in Path(origin).parts) or Path(origin).suffix in ('.pem', '.key')):
            raise ValueError('Private distribution source forbidden')
        for mapped in (destination, origin):
            if isinstance(mapped, str) and (set(Path(mapped).parts) & {'.tmp', 'dist', '.idea', '.venv', 'node_modules', '__pycache__', '.DS_Store'} or Path(mapped).suffix in ('.pyc', '.pyo', '.pyd')):
                raise ValueError('Generated/local files cannot be distributed: ' + mapped)
        if not source_path(root, origin).is_file():
            raise ValueError('Distribution source file missing: ' + str(origin))
    return manifest, source, market, extra


def payload():
    manifest, skill_root, market, extra = configuration()
    # Host metadata is derived from the portable manifest; no duplicate version source.
    claude = {key: manifest[key] for key in ('name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords') if key in manifest}
    files = {}
    def collect(folder, destination):
        if not folder.exists():
            return
        if folder.is_symlink():
            raise ValueError('Symlink in distributable source')
        for path in sorted(folder.rglob('*')):
            relative = path.relative_to(folder)
            if path.is_symlink():
                raise ValueError(f'Symlink in distributable source: {relative}')
            if any(part.startswith('.env') for part in relative.parts) or path.suffix in ('.key', '.pem'):
                raise ValueError(f'Private file in distributable source: {relative}')
            if any(part.startswith('.') or part in ('__pycache__','node_modules','dist') for part in relative.parts) or path.suffix in ('.pyc', '.pyo', '.pyd'):
                continue
            if path.is_file():
                files[str(Path(destination) / relative)] = read_file(path)
    collect(skill_root, 'skills')
    collect(ROOT / 'assets', 'assets')
    for name in ('LICENSE', 'LICENSE.md', 'LICENSE.txt'):
        if (ROOT / name).exists():
            files[name] = read_file(ROOT / name)
    for destination, origin in extra.items():
        data = read_file(source_path(ROOT, origin))
        if destination in files and files[destination] != data:
            raise ValueError('Conflicting distribution destination: ' + destination)
        files[destination] = data
    # Default package description is derived, not another manually maintained README.
    files.setdefault('README.md', ('# ' + manifest['name'] + '\n\n' + manifest['description'] +
        '\n\nThis plugin bundles its canonical skills. Activate it in your host and ask for its capabilities. '
        'Its source instructions define usage and limitations. Local packaging does not publish or install the plugin. '
        'Review host permissions and test behavior before deploying to production.\n').encode())
    commands = {}
    if (ROOT / 'commands').is_symlink():
        raise ValueError('Commands directory must not be a symlink')
    for path in sorted((ROOT / 'commands').glob('*.md')):
        commands['commands/' + path.name] = read_file(path)
    onboarding = manifest.get('extensions', {}).get('com.openai', {}).get('onboardingSkill')
    if onboarding and onboarding.removeprefix('./') not in files:
        raise ValueError('onboardingSkill does not exist in packaged payload')
    interface = manifest.get('extensions', {}).get('com.openai', {}).get('interface', {})
    for field in ('logo', 'composerIcon'):
        value = interface.get(field)
        if value and value.removeprefix('./') not in files:
            raise ValueError('Host asset missing from payload: ' + field)
    fingerprint = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode())
    for name, content in sorted({**files, **commands}.items()):
        fingerprint.update(name.encode() + b'\0' + content + b'\0')
    version = manifest['version'] + '-dev.h' + fingerprint.hexdigest()[:12]
    manifest['version'] = claude['version'] = version
    # Local build configuration is not a runtime host extension.
    if 'extensions' in manifest:
        manifest['extensions'].pop(CONFIG_KEY, None)
    encode = lambda data: (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()
    return version, dict(files, **{'plugin.json': encode(manifest)}), dict(files, **commands, **{'.claude-plugin/plugin.json': encode(claude)})


def codex_payload(portable):
    manifest = json.loads(portable['plugin.json'])
    codex = {key: manifest[key] for key in ('name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords') if key in manifest}
    codex['skills'] = './skills/'
    interface = manifest.get('extensions', {}).get('com.openai', {}).get('interface')
    if interface:
        codex['interface'] = interface
    files = {name: content for name, content in portable.items() if name != 'plugin.json'}
    files['.codex-plugin/plugin.json'] = (json.dumps(codex, ensure_ascii=False, indent=2) + '\n').encode()
    return files


def archive(path, files):
    fd, temporary = tempfile.mkstemp(prefix='.zip-', dir=path.parent)
    os.close(fd)
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED) as output:
            for name, content in sorted(files.items()):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                output.writestr(info, content)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def marketplace(path, files, version, platform="claude"):
    manifest, _, market, _ = configuration()
    name = manifest['name']
    if path.is_symlink() or (path.exists() and not owned_marketplace(path)):
        raise ValueError(f'Refusing to replace an unowned marketplace: {path}')
    staged = Path(tempfile.mkdtemp(prefix='.marketplace-', dir=path.parent))
    backup = None
    try:
        (staged / MARKER).write_text(name + '\n')
        plugin_root = staged / 'plugins' / name
        for relative, content in files.items():
            target = plugin_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        catalog = {'name': market, 'metadata': {'description': manifest['description']},
                   'owner': {'name': manifest.get('author', {}).get('name', manifest['name'])},
                   'plugins': [{'name': name, 'source': './plugins/' + name, 'version': version,
                                'description': manifest['description']}]}
        if platform == 'codex':
            catalog = {'name': market, 'plugins': [
                {'name': name, 'source': {'source': 'local', 'path': './plugins/' + name},
                 'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}}]}
        catalog_path = staged / ('.agents/plugins/marketplace.json' if platform == 'codex' else '.claude-plugin/marketplace.json')
        catalog_path.parent.mkdir(parents=True)
        catalog_path.write_text(json.dumps(catalog, indent=2) + '\n')
        if path.exists():
            backup = Path(tempfile.mkdtemp(prefix='.marketplace-backup-', dir=path.parent))
            backup.rmdir()
            path.rename(backup)
        try:
            staged.rename(path)
        except OSError:
            if backup:
                backup.rename(path)
                backup = None
            raise
    finally:
        if staged.exists():
            shutil.rmtree(staged)
        if backup and backup.exists():
            shutil.rmtree(backup)


def owned_marketplace(path):
    marker = path / MARKER
    return marker.is_file() and not marker.is_symlink() and marker.read_text().strip() == configuration()[0]['name']


def build(output=None):
    name = configuration()[0]['name']
    version, openai, claude = payload()
    output = Path(output) if output else ROOT / 'dist'
    if output.is_symlink():
        raise ValueError('Build output must not be a symlink')
    output.mkdir(parents=True, exist_ok=True)
    market = output / 'claude-marketplace'
    codex_market = output / 'codex-marketplace'
    for destination in (market, codex_market):
        if destination.is_symlink() or (destination.exists() and not owned_marketplace(destination)):
            raise ValueError('Build destination contains an unowned marketplace')
    codex = codex_payload(openai)
    for platform, files in (('chatgpt', openai), ('claude', claude), ('codex', codex)):
        path = output / f'{name}-{platform}-plugin.zip'
        if path.is_symlink():
            raise ValueError('Package output must not be a symlink')
        archive(path, files)
    marketplace(market, claude, version)
    marketplace(codex_market, codex, version, platform='codex')
    return {'version': version, 'output': str(output.resolve()),
            'chatgpt_zip': str((output / f'{name}-chatgpt-plugin.zip').resolve()),
            'claude_zip': str((output / f'{name}-claude-plugin.zip').resolve()),
            'claude_marketplace': str(market.resolve()),
            'codex_zip': str((output / f'{name}-codex-plugin.zip').resolve()),
            'codex_marketplace': str(codex_market.resolve()),
            'published': False}


def install(target, update=False, dry_run=False):
    if target not in ('claude', 'chatgpt', 'codex'):
        raise ValueError('Unsupported plugin host')
    manifest, _, market, _ = configuration()
    name = manifest['name']
    artifacts = build()
    if target == 'chatgpt':
        return {'artifacts': artifacts, 'installed': False,
                'next': 'Manually upload the ChatGPT plugin ZIP, or Upload new version in plugin administration. Required account/workspace permissions apply. No upload was performed.'}
    if target == 'codex':
        # Re-register the local source and install the content-derived version.
        # No uninstall and no Git marketplace upgrade are needed for local sources.
        commands = [['codex', 'plugin', 'marketplace', 'add', artifacts['codex_marketplace'], '--json'],
                    ['codex', 'plugin', 'add', name + '@' + market, '--json']]
    elif update:
        commands = [['claude', 'plugin', 'marketplace', 'update', market],
                    ['claude', 'plugin', 'update', name + '@' + market, '--scope', 'user']]
    else:
        commands = [['claude', 'plugin', 'install', name, '--marketplace', artifacts['claude_marketplace'], '--scope', 'user']]
    if not dry_run:
        if not shutil.which(target):
            raise ValueError(f'{target} CLI not found. Packages were built; install a CLI with native plugin support before running this target.')
        for command in commands:
            subprocess.run(command, check=True)
    return {'artifacts': artifacts, 'commands': commands, 'executed': not dry_run,
            'next': ('Open a new Codex chat, or restart Codex if the plugin is not visible. The local marketplace must remain available for updates.' if target == 'codex' else 'Restart Claude Code. For updates, install this local marketplace once first.')}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    package = sub.add_parser('build')
    package.add_argument('--output', type=Path)
    for command in ('install', 'update'):
        action = sub.add_parser(command)
        action.add_argument('--target', choices=('claude', 'chatgpt', 'codex'), default='claude')
        action.add_argument('--dry-run', action='store_true')
    check = sub.add_parser('check')
    args = parser.parse_args(argv)
    try:
        result = ({'valid': True, 'name': configuration()[0]['name'], 'version': payload()[0]} if args.command == 'check' else build(args.output) if args.command == 'build' else install(args.target, args.command == 'update', args.dry_run))
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
