import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('documentation', ROOT / 'skills/zyris-skill-manager/scripts/documentation.py')
doc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(doc)


class DocumentationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        (self.source / 'SKILL.md').write_text('---\nname: fictional-demo\n---\n# Demo\nA fictional test skill.\n')
        self.output = self.root / 'output'

    def fill(self):
        for name in doc.outline():
            path = self.output / name
            text = path.read_text()
            text = re.sub(r'\{\{[^}]+\}\}', 'Verified fictional example.', text)
            path.write_text(text)

    def test_inspect_resolves_canonical_skill_not_root_pointer(self):
        repo = self.root / 'repository'
        skill = repo / '.claude/skills/example'
        skill.mkdir(parents=True)
        (repo / 'SKILL.md').write_text('# Compatibility pointer')
        (skill / 'SKILL.md').write_text('---\nname: example\n---\n')
        self.assertEqual(doc.source_skill(repo), skill.resolve())
        second = repo / 'skills/other'
        second.mkdir(parents=True)
        (second / 'SKILL.md').write_text('---\nname: other\n---\n')
        with self.assertRaisesRegex(ValueError, 'Select one'):
            doc.inspect(repo)

    def test_scaffold_is_bilingual_preserves_existing_and_copies_exact_icon(self):
        result = doc.scaffold(self.source, self.output, languages=['de','en'])
        self.assertEqual(len(doc.outline()), 16)
        self.assertEqual(len(result['created']), 18)
        self.assertEqual((self.output / 'docs/assets/zyris-icon.png').read_bytes(), doc.icon_source().read_bytes())
        (self.output / 'README.md').write_text('Existing user content')
        self.assertEqual(doc.scaffold(self.source, self.output, languages=['de','en'])['created'], [])
        self.assertEqual((self.output / 'README.md').read_text(), 'Existing user content')

    def test_validation_rejects_unwritten_scaffold_then_accepts_complete_structure(self):
        doc.scaffold(self.source, self.output, languages=['de','en'])
        self.assertTrue(any('placeholders' in item for item in doc.validate(self.output)))
        self.fill()
        self.assertEqual(doc.validate(self.output), [])

    def test_validation_detects_broken_links_missing_locale_and_heading_drift(self):
        doc.scaffold(self.source, self.output, languages=['de','en'])
        self.fill()
        page = self.output / 'docs/en/usage.md'
        page.write_text(page.read_text().replace('## Set up', '## Changed heading') + '\n[Broken](missing.md)\n')
        (self.output / 'README.en.md').unlink()
        errors = '\n'.join(doc.validate(self.output))
        self.assertIn('missing page', errors)
        self.assertIn('missing link target', errors)
        self.assertIn('headings', errors)

    def test_validation_checks_language_switch_and_anchor(self):
        doc.scaffold(self.source, self.output, languages=['de','en'])
        self.fill()
        page = self.output / 'docs/en/screens.md'
        page.write_text(page.read_text().replace('[Deutsch](../de/screens.md)', 'Deutsch') + '\n[Missing section](usage.md#does-not-exist)\n')
        errors = '\n'.join(doc.validate(self.output))
        self.assertIn('counterpart', errors)
        self.assertIn('heading anchor', errors)

    def test_refuses_skill_output_symlinks_and_custom_icon_overwrite(self):
        with self.assertRaisesRegex(ValueError, 'outside'):
            doc.scaffold(self.source, self.source, languages=['de','en'])
        self.output.mkdir()
        (self.output / 'docs').symlink_to(self.source, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            doc.scaffold(self.source, self.output, languages=['de','en'])
        self.assertFalse((self.output / 'README.md').exists())
        (self.output / 'docs').unlink()
        icon = self.output / 'docs/assets/zyris-icon.png'
        icon.parent.mkdir(parents=True)
        icon.write_bytes(b'custom')
        with self.assertRaisesRegex(ValueError, 'differs'):
            doc.scaffold(self.source, self.output, languages=['de','en'])
        self.assertEqual(icon.read_bytes(), b'custom')
        self.assertFalse((self.output / 'README.md').exists())

    def test_english_and_german_templates_have_localized_headings(self):
        outline = doc.outline()
        self.assertEqual(outline['README.md'][0], 'Für wen ist das gedacht?')
        self.assertEqual(outline['README.en.md'][0], 'Who it is for')
        self.assertEqual(outline['docs/de/screens.md'][0], 'Vorschau')
        self.assertEqual(outline['docs/en/screens.md'][0], 'Preview')

    def test_manifest_selects_source_without_caching_product_facts(self):
        repo = self.root / 'repository'
        selected = repo / 'skills/one'
        selected.mkdir(parents=True)
        (selected / 'SKILL.md').write_text('---\nname: one\n---\n')
        other = repo / 'skills/two'
        other.mkdir()
        (other / 'SKILL.md').write_text('---\nname: two\n---\n')
        doc.scaffold(selected, repo, languages=['de','en'])
        manifest_path = repo / 'docs/documentation.json'
        data = json.loads(manifest_path.read_text())
        self.assertEqual(data['source_skill'], 'skills/one')
        self.assertEqual(doc.source_skill(repo), selected.resolve())
        data['features'] = ['A duplicated unsupported claim']
        manifest_path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'not duplicated'):
            doc.inspect(repo)

    def test_manifest_rejects_missing_and_external_sources(self):
        repo = self.root / 'repository'
        (repo / 'docs').mkdir(parents=True)
        path = repo / 'docs/documentation.json'
        for pointer in ('missing', '../source'):
            path.write_text(json.dumps({'schema_version':1,'source_skill':pointer}))
            with self.subTest(pointer=pointer), self.assertRaises(ValueError):
                doc.inspect(repo)

    def test_single_language_and_english_default_layouts(self):
        for languages, default in ((['en'],'en'), (['de'],'de'), (['en','de'],'en')):
            with self.subTest(languages=languages):
                output = self.root / ('-'.join(languages))
                doc.scaffold(self.source, output, languages=languages, default_language=default)
                policy = doc.language_policy(output)
                pages = doc.page_layout(policy)
                self.assertEqual(8 * len(languages),len(pages))
                for name in pages:
                    path = output / name
                    path.write_text(re.sub(r'\{\{[^}]+\}\}', 'Fictional example.', path.read_text()))
                self.assertEqual([],doc.validate(output))
                self.assertIn('## Who it is for' if default=='en' else '## Für wen ist das gedacht?',(output/'README.md').read_text())
                if len(languages)==1:
                    self.assertFalse((output/'README.en.md').exists())
                    self.assertFalse((output/'README.de.md').exists())
                    other='de' if default=='en' else 'en'
                    self.assertFalse((output/'docs'/other).exists())
                else:
                    self.assertTrue((output/'README.de.md').is_file())
                self.assertEqual([],doc.scaffold(self.source,output)['created'])

    def test_policy_rejects_invalid_or_conflicting_choices_before_writes(self):
        for languages,default in (([], 'en'),(['en','en'],'en'),(['fr'],'fr'),(['en'],'de')):
            with self.assertRaises(ValueError):
                doc.scaffold(self.source,self.output,languages=languages,default_language=default)
            self.assertFalse(self.output.exists())
        doc.scaffold(self.source,self.output,languages=['en'])
        (self.output/'README.md').write_text('Preserve this text')
        with self.assertRaisesRegex(ValueError,'conflicts'):
            doc.scaffold(self.source,self.output,languages=['de'])
        self.assertEqual('Preserve this text',(self.output/'README.md').read_text())

    def test_selected_language_cannot_hide_broken_links(self):
        doc.scaffold(self.source,self.output,languages=['en'])
        for name in doc.page_layout(doc.language_policy(self.output)):
            path=self.output/name
            path.write_text(re.sub(r'\{\{[^}]+\}\}', 'Fictional example.', path.read_text()))
        page=self.output/'README.md'
        page.write_text(page.read_text()+'\n[Accidental unselected language](README.de.md)\n')
        self.assertIn('missing link target','\n'.join(doc.validate(self.output)))

    def test_new_project_requires_language_decision_before_writes(self):
        with self.assertRaisesRegex(ValueError,'Choose documentation languages'):
            doc.scaffold(self.source,self.output)
        self.assertFalse(self.output.exists())
