#!/usr/bin/env python3
"""Read-only plugin structure audit and non-overwriting initialization."""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys
sys.dont_write_bytecode = True

from documentation import SKILL, inspect, scaffold, icon_source, validate
from repository_policy import hygiene, python_payload

UNSAFE = {'.env', '.git', '.tmp', '.DS_Store', '__pycache__', 'node_modules', 'dist'}


def candidates(root):
    result = {}
    for folder in ('skills', '.claude/skills', '.agents/skills'):
        for path in sorted((root / folder).glob('*/SKILL.md')):
            result.setdefault(path.parent.name, set()).add(path.parent.resolve())
    return result


def audit(root):
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError('Plugin repository directory not found')
    checks = []
    def add(code, status, message):
        checks.append({'id': code, 'status': status, 'message': message})
    manifests = []
    for relative in ('plugin.json', '.claude-plugin/plugin.json'):
        path = root / relative
        if path.is_file():
            try:
                data = json.loads(path.read_text(encoding='utf-8'))
                if not isinstance(data, dict) or not isinstance(data.get('name'), str) or not data['name'] or not isinstance(data.get('description'), str) or not data['description']:
                    raise ValueError('name and description required')
                if 'version' in data and not isinstance(data['version'], str):
                    raise ValueError('version must be a string')
                manifests.append(data)
                add(relative, 'pass', 'Manifest is parseable and declares name/description')
            except (ValueError, OSError) as exc:
                add(relative, 'fail', str(exc))
    if not manifests:
        add('plugin_manifest', 'fail', 'No valid portable or Claude plugin manifest found')
    else:
        names = {value['name'] for value in manifests}
        versions = {value.get('version') for value in manifests if value.get('version')}
        add('identity', 'pass' if len(names) == 1 else 'fail', 'Plugin manifest names must agree')
        add('version', 'pass' if not versions else 'fail', 'Repository updates follow commits; omit manifest versions')
    # Inspect legacy layouts, but never certify them as the common source layout.
    layout_issues = []
    portable = root / 'plugin.json'
    if portable.is_file():
        try:
            config = json.loads(portable.read_text()).get('extensions', {}).get('io.zyris.distribution', {})
            if config.get('skillRoot', 'skills') != 'skills':
                layout_issues.append('skillRoot must be skills')
        except (ValueError, AttributeError):
            layout_issues.append('Cannot resolve neutral skillRoot from plugin.json')
    else:
        layout_issues.append('Root plugin.json is required')
    for folder in ('.claude/skills', '.agents/skills'):
        if (root / folder).exists():
            layout_issues.append('Migrate host-local source ' + folder + ' to skills/')
    add('neutral_source_layout', 'fail' if layout_issues else 'pass',
        '; '.join(layout_issues) if layout_issues else 'Host-neutral skills/ source; committed host metadata is checked separately')
    skills = candidates(root)
    add('skills', 'pass' if skills else 'fail', 'At least one canonical skill with SKILL.md is required')
    duplicates = [name for name, paths in skills.items() if len(paths) > 1]
    add('source_of_truth', 'fail' if duplicates else 'pass', 'Duplicate canonical skill names: ' + ', '.join(duplicates) if duplicates else 'No parallel skill copies with the same name detected; semantic drift still requires review')
    for name, paths in skills.items():
        for path in paths:
            text = (path / 'SKILL.md').read_text(encoding='utf-8')
            front = text.split('---', 2)
            valid = (text.startswith('---\n') and len(front) == 3
                     and re.search(r'^name:\s*\S', front[1], re.MULTILINE)
                     and re.search(r'^description:\s*\S', front[1], re.MULTILINE))
            add('skill:' + name, 'pass' if valid else 'fail', 'Skill requires name/description frontmatter')
            suspicious = []
            for item in path.rglob('*'):
                if item.is_symlink() or item.name in (UNSAFE - {'__pycache__'}) or item.name.startswith('.env.') or item.suffix in ('.pem', '.key'):
                    suspicious.append(str(item.relative_to(path)))
            add('payload:' + name, 'fail' if suspicious else 'pass', 'Review unsafe/unexpected distributable paths: ' + ', '.join(suspicious) if suspicious else 'No obvious secret or unexpected paths or symlinks; ordinary Python caches are excluded by the validated builder, not a secret-content scan')
    # Load our trusted template, never the target repository's executable code.
    template = SKILL / 'templates/plugin'
    for relative in ('scripts/plugin.py', 'install.sh', 'plugin.mk'):
        target = root / relative
        matches = target.is_file() and not target.is_symlink() and target.read_bytes() == (template / relative).read_bytes()
        add('installer:' + relative, 'pass' if matches else 'fail',
            'Matches canonical installer template' if matches else 'Missing or divergent installer; review and regenerate from documentation plugin template')
    makefile = root / 'Makefile'
    make = makefile.read_text() if makefile.is_file() else ''
    delegates = bool(re.search(r'^include plugin\.mk\s*$', make, re.MULTILINE))
    overrides = bool(re.search(r'^(?:install|update|package|check-plugin|sync-plugin)\s*:', make, re.MULTILINE))
    add('installer:make', 'pass' if delegates and not overrides else 'fail', 'Makefile must include plugin.mk without overriding its installation recipes')
    try:
        spec = importlib.util.spec_from_file_location('trusted_plugin_template', template / 'scripts/plugin.py')
        engine = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(engine)
        engine.ROOT = root
        engine.repository_metadata(check=True)
        _, portable, _ = engine.payload()  # In-memory only; never execute target code.
        py_errors, py_warnings = python_payload(portable)
        add('python_payload', 'fail' if py_errors else ('warning' if py_warnings else 'pass'),
            '; '.join(py_errors + py_warnings) if py_errors or py_warnings else
            'Packaged Python syntax and static imports checked; dynamic dependencies and host execution still require tests')
        add('installer:manifest', 'pass', 'Distribution configuration and payload resolve from plugin.json')
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        add('installer:manifest', 'fail', str(exc))
    for label, present, message in (
        ('build', (root / 'Makefile').is_file() and (root / 'scripts').is_dir(), 'Build entry point and development scripts'),
        ('tests', any((root / 'tests').rglob('test_*.py')), 'Deterministic test files; existence does not prove coverage or passing execution'),
        ('ci', any((root / '.github/workflows').glob('*.yml')), 'CI workflow; not proof of a successful remote run'),
        ('license', any((root / name).is_file() for name in ('LICENSE','LICENSE.md','LICENSE.txt')), 'Explicit licensing decision; do not invent terms')):
        add(label, 'pass' if present else 'warning', message)
    hygiene_errors, hygiene_warnings = hygiene(root)
    add('repository_hygiene', 'fail' if hygiene_errors else ('warning' if hygiene_warnings else 'pass'),
        '; '.join(hygiene_errors + hygiene_warnings) if hygiene_errors or hygiene_warnings else
        'Required ignore rules effective; no tracked local/generated files detected')
    try:
        errors = validate(root)
        add('documentation', 'warning' if errors else 'pass', '; '.join(errors) if errors else 'Configured languages, structure, links and brand icon checked')
    except (OSError, ValueError) as exc:
        add('documentation', 'warning', str(exc))
    try:
        from documentation import read_manifest, exporter
        manifest = read_manifest(root)
        if manifest and 'export' in manifest:
            matches = all((root / relative).is_file() and not (root / relative).is_symlink()
                          and (root / relative).read_bytes() == (template / relative).read_bytes()
                          for relative in ('scripts/export_docs.py', 'docs.mk'))
            matches = matches and 'include docs.mk' in make
            add('documentation_export_tooling', 'pass' if matches else 'fail',
                'Exporter and Make integration must match the canonical documentation template')
            exporter().build_files(root)
            add('documentation_export_contract', 'pass', 'Selected pages, assets, links and derived metadata form a valid export')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        add('documentation_export_contract', 'fail', str(exc))
    manual = [
        'Run appropriate tests and inspect their actual output; audit does not execute target code.',
        'Test Python entry points from an installed copy outside the checkout; verify dynamic imports, dependencies, supported Python and filesystem ownership.',
        'Test repository import, update, permissions and uninstall in each supported host; development archive tests are optional.',
        'Verify product behavior, storage/privacy boundaries and unsupported claims.',
        'Review distribution/licensing decisions and required publisher metadata.',
        'Review German/English equivalence and screenshot provenance.'
    ]
    failed = any(item['status'] == 'fail' for item in checks)
    warnings = any(item['status'] == 'warning' for item in checks)
    return {'structurally_valid': not failed, 'production_ready': None,
            'status': 'needs_attention' if failed or warnings else 'structure_passed_acceptance_pending',
            'checks': checks, 'manual_checks_not_verified': manual,
            'target_code_executed': False}


def initialize(source, output, languages=None, default_language=None, repository=None, author=None):
    from documentation import language_policy
    language_policy(Path(output).expanduser().resolve(), languages, default_language)
    info = inspect(source)
    source = Path(info['skill'])
    output = Path(output).expanduser().absolute()
    if any(part.is_symlink() for part in (output, *output.parents)):
        raise ValueError('Output path must not contain symlinks')
    output = output.resolve()
    if output.is_relative_to(source) or source.is_relative_to(output):
        raise ValueError('Use a separate output repository; existing sources are never moved')
    if output.exists() and any(p.name not in ('.git', '.idea', '.DS_Store') for p in output.iterdir()):
        raise ValueError('Output repository is not empty. Run verify, then make reviewed targeted changes; init never overwrites')
    name = info['name']
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('Source skill name must use lowercase kebab-case')
    files = {}
    for path in source.rglob('*'):
        relative = path.relative_to(source)
        if path.is_symlink():
            raise ValueError(f'Review source symlink before packaging: {relative}')
        if any(part in UNSAFE or part.startswith('.env.') for part in relative.parts):
            raise ValueError(f'Remove private/cache/build paths from input skill: {relative}')
        if path.is_file():
            if path.suffix in ('.pem','.key'):
                raise ValueError(f'Private key-like file in source: {relative}')
            files[str(Path('skills') / name / relative)] = path.read_bytes()
    manifest = {'$schema': 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', 'name': name, 'description': f'Plugin bundling the {name} skill.',
                'extensions': {'io.zyris.distribution': {'skillRoot': 'skills'}}}
    if repository:
        if not re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
            raise ValueError('Use a verified GitHub repository URL without credentials')
        manifest['repository'] = repository
    if author:
        manifest['author'] = {'name': author}
    spec = importlib.util.spec_from_file_location('init_plugin_template', SKILL / 'templates/plugin/scripts/plugin.py')
    engine = importlib.util.module_from_spec(spec); spec.loader.exec_module(engine)
    for relative, data in engine.repository_files(manifest).items():
        files[relative] = (json.dumps(data, indent=2) + '\n').encode()
    files['plugin.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    files['assets/icon.png'] = icon_source().read_bytes()
    template_root = SKILL / 'templates/plugin'
    for path in template_root.rglob('*'):
        if path.is_file():
            relative = str(path.relative_to(template_root))
            if relative == 'gitignore.txt':
                relative = '.gitignore'
            if relative == 'ci.yml':
                relative = '.github/workflows/validate.yml'
            files[relative] = path.read_bytes()
    # Preflight every destination; init never replaces any pre-existing file.
    for relative in files:
        target = output / relative
        if target.exists() or target.is_symlink():
            raise ValueError(f'Existing file: {target}')
    for relative, content in files.items():
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as handle:
            handle.write(content)
    scaffold(output / 'skills' / name, output, name, languages, default_language)
    return {'initialized': str(output), 'source_preserved': str(source),
            'production_ready': None,
            'next': 'Confirm repository URL and publisher metadata before import; do not invent them. Author the selected documentation languages, inspect manifests, add behavior-specific tests and validate hosts. Boilerplate checks alone do not establish production readiness.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    verify = sub.add_parser('verify')
    verify.add_argument('--source', type=Path, required=True)
    init = sub.add_parser('init')
    init.add_argument('--source', type=Path, required=True)
    init.add_argument('--output', type=Path, required=True)
    init.add_argument('--repository')
    init.add_argument('--author')
    init.add_argument('--languages', nargs='+', choices=('de','en'))
    init.add_argument('--default-language', choices=('de','en'))
    args = parser.parse_args(argv)
    try:
        result = audit(args.source) if args.command == 'verify' else initialize(args.source, args.output, args.languages, args.default_language, args.repository, args.author)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return int(args.command == 'verify' and result['status'] == 'needs_attention')
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
