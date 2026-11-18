import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('plugin_build', ROOT / 'scripts/plugin.py')
plugin = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(plugin)


class PluginTests(unittest.TestCase):
    def test_packages_are_plugins_with_bundled_templates_icon_and_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            result = plugin.build(Path(directory))
            for platform, key in (('claude', '.claude-plugin/plugin.json'), ('chatgpt', 'plugin.json')):
                with zipfile.ZipFile(result[platform + '_zip']) as archive:
                    names = archive.namelist()
                    self.assertIn(key, names)
                    self.assertNotIn('install.sh', names)
                    self.assertFalse(any('.git/' in name or name.startswith('tests/') for name in names))
                    manifest = json.loads(archive.read(key))
                    self.assertEqual(manifest['version'], result['version'])
                    prefix = 'skills/zyris-skill-documentation/'
                    for path in ('SKILL.md', 'scripts/documentation.py', 'templates/README.md',
                                 'templates/README.en.md', 'templates/docs/de/screens.md', 'templates/docs/en/screens.md'):
                        self.assertIn(prefix + path, names)
                    self.assertEqual(archive.read('assets/icon.png'), archive.read(prefix + 'assets/icon.png'))
            catalog = Path(result['claude_marketplace']) / '.claude-plugin/marketplace.json'
            self.assertEqual(json.loads(catalog.read_text())['plugins'][0]['version'], result['version'])

    def test_rebuild_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            first = plugin.build(Path(directory))
            original = Path(first['chatgpt_zip']).read_bytes()
            second = plugin.build(Path(directory))
            self.assertEqual(first['version'], second['version'])
            self.assertEqual(original, Path(second['chatgpt_zip']).read_bytes())

    def test_runtime_change_changes_cache_version(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder in ('skills', 'assets'):
                shutil.copytree(ROOT / folder, root / folder)
            shutil.copy2(ROOT / 'plugin.json', root / 'plugin.json')
            with patch.object(plugin, 'ROOT', root):
                before = plugin.payload()[0]
                with (root / 'skills/zyris-skill-documentation/references/style.md').open('a') as handle:
                    handle.write('\nA revised documentation rule.\n')
                after = plugin.payload()[0]
                self.assertNotEqual(before, after)

    def test_extracted_chatgpt_plugin_scaffolds_without_developer_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = plugin.build(root / 'build')
            with zipfile.ZipFile(result['chatgpt_zip']) as archive:
                archive.extractall(root / 'installed')
            helper = root / 'installed/skills' / 'zyris-skill-documentation' / 'scripts/documentation.py'
            source = root / 'fictional'
            source.mkdir()
            (source / 'SKILL.md').write_text('---\nname: fictional\n---\n# Fictional skill')
            result = subprocess.run([sys.executable, str(helper), 'scaffold', '--source', str(source),
                                     '--output', str(root / 'docs-output'), '--languages', 'de', 'en'], capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / 'docs-output/README.en.md').is_file())
            self.assertEqual((root / 'docs-output/docs/assets/zyris-icon.png').read_bytes(), (ROOT / 'assets/icon.png').read_bytes())

    def test_chatgpt_install_never_claims_upload_or_runs_host(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(plugin, 'build', return_value={'chatgpt_zip':directory}), patch.object(plugin.subprocess, 'run') as run:
            result = plugin.install('chatgpt', update=True)
            self.assertFalse(result['installed'])
            run.assert_not_called()
            self.assertIn('Manually', result['next'])

    def test_native_claude_install_and_update_commands(self):
        with patch.object(plugin, 'build', return_value={'claude_marketplace':'/fictional/market'}), patch.object(plugin.shutil, 'which', return_value='claude'), patch.object(plugin.subprocess, 'run') as run:
            plugin.install('claude')
            self.assertIn('--marketplace', run.call_args.args[0])
            self.assertNotIn('skills', ' '.join(run.call_args.args[0]))
            run.reset_mock()
            plugin.install('claude', update=True)
            self.assertEqual(run.call_count, 2)
            self.assertEqual(run.call_args_list[0].args[0][1:4], ['plugin','marketplace','update'])
            self.assertEqual(run.call_args_list[1].args[0][1:3], ['plugin','update'])
            run.reset_mock()
            plugin.install('claude', dry_run=True)
            run.assert_not_called()

    def test_foreign_marketplace_and_symlink_sources_are_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            market = root / 'claude-marketplace'
            market.mkdir()
            (market / 'user.txt').write_text('preserve')
            with self.assertRaisesRegex(ValueError, 'unowned'):
                plugin.build(root)
            self.assertEqual((market / 'user.txt').read_text(), 'preserve')
            with self.assertRaises(ValueError):
                plugin.read_file(market)
