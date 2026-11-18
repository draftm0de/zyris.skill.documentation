#!/usr/bin/env python3
"""Opt-in native tests of generated bundles in disposable profiles. No model calls."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
sys.dont_write_bytecode = True
import release


def check(bundles, output):
    records = [release.verify_bundle(bundle, True) for bundle in bundles]
    names = [record['name'] for record in records]
    evidence = []
    with tempfile.TemporaryDirectory(prefix='zyris-native-') as temporary:
        work = Path(temporary)
        catalog = work / 'catalog'; release.catalog(bundles, catalog, True)
        env = dict(os.environ)
        for variable, folder in [('HOME', 'home'), ('CODEX_HOME', 'codex-home'), ('CLAUDE_CONFIG_DIR', 'claude-home')]:
            env[variable] = str(work / folder); Path(env[variable]).mkdir()
        private = work / 'private-progress.json'; private.write_text('{"fictional":true}')
        original = release.snapshot(catalog)
        def run(*args):
            p = subprocess.run(args, cwd=work, env=env, capture_output=True, text=True, timeout=90)
            evidence.append({'command': list(args), 'exit': p.returncode})
            if p.returncode: raise RuntimeError(p.stderr or p.stdout)
            return p.stdout
        def verify_installed(version_by_name):
            for name in names:
                installed = json.loads(run('codex', 'plugin', 'add', name + '@zyris', '--json'))
                assert installed['version'] == version_by_name[name]
                source = catalog / 'plugins' / name
                cache = Path(installed['installedPath'])
                for path in (source / 'skills').rglob('*'):
                    if path.is_file(): assert (cache / path.relative_to(source)).read_bytes() == path.read_bytes()
            installed = json.loads(run('claude', 'plugin', 'list', '--json'))
            assert len(installed) == len(names)
            for item in installed:
                name = item['id'].split('@')[0]
                assert item['version'] == version_by_name[name]
                source = catalog / 'plugins' / name
                cache = Path(item.get('readFromFolder') or item['installPath'])
                for path in (source / 'skills').rglob('*'):
                    if path.is_file(): assert (cache / path.relative_to(source)).read_bytes() == path.read_bytes()
        try:
            run('codex', 'plugin', 'marketplace', 'add', str(catalog), '--json')
            run('claude', 'plugin', 'marketplace', 'add', str(catalog))
            for name in names: run('claude', 'plugin', 'install', name + '@zyris', '--scope', 'user')
            verify_installed({r['name']: r['version'] for r in records})
            for patch_number in (1, 2):
                # B changes runtime content; C restores exact A runtime with a higher test version.
                for relative, data in original.items():
                    path = catalog / relative
                    if relative.endswith('/SKILL.md') and patch_number == 1:
                        data += b'\nFictional native update test marker.\n'
                    path.write_bytes(data)
                versions = {}
                for record in records:
                    name = record['name']; base = record['version'].split('-')[0].split('.')
                    version = '.'.join(base[:2] + [str(int(base[2]) + patch_number)])
                    versions[name] = version
                    for host in ('claude', 'codex'):
                        path = catalog / 'plugins' / name / f'.{host}-plugin/plugin.json'
                        metadata = json.loads(path.read_text()); metadata['version'] = version; path.write_bytes(release.encode(metadata))
                path = catalog / '.claude-plugin/marketplace.json'; metadata = json.loads(path.read_text())
                for entry in metadata['plugins']: entry['version'] = versions[entry['name']]
                path.write_bytes(release.encode(metadata))
                run('codex', 'plugin', 'marketplace', 'add', str(catalog), '--json')
                run('claude', 'plugin', 'marketplace', 'update', 'zyris')
                for name in names: run('claude', 'plugin', 'update', name + '@zyris', '--scope', 'user')
                verify_installed(versions)
                assert private.read_text() == '{"fictional":true}'
            for name in names:
                run('codex', 'plugin', 'remove', name + '@zyris', '--json')
                run('claude', 'plugin', 'uninstall', name + '@zyris', '--scope', 'user')
            assert not json.loads(run('codex', 'plugin', 'list', '--marketplace', 'zyris', '--json'))['installed']
            assert not json.loads(run('claude', 'plugin', 'list', '--json'))
            assert private.read_text() == '{"fictional":true}'
            evidence.append({'passed': True, 'products': names, 'local_preview_only': True,
                             'runtime_update_and_forward_recovery': True, 'private_data_preserved': True})
        finally:
            path = Path(output); path.parent.mkdir(parents=True, exist_ok=True)
            # Do not export personal paths or full host output; only generated test commands/results.
            text = json.dumps(evidence, indent=2).replace(str(work), 'ISOLATED_TEST_ROOT')
            path.write_text(text + '\n')
    return evidence[-1]

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle', action='append', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    print(json.dumps(check(args.bundle, args.output), indent=2))
