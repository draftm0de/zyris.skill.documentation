"""Read-only repository hygiene and static packaged-Python checks.

Git ignore semantics are evaluated in an isolated temporary repository. No target
hooks, scripts, global excludes or target index mutations are used.
"""
import ast
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile

IGNORED_DIRS = {'.tmp', 'dist', '.idea', '__pycache__', '.venv', 'node_modules'}
PROBES = ('.DS_Store', '.idea/workspace.xml', '.tmp/probe', 'dist/probe',
          '__pycache__/probe.pyc', 'probe.pyc', 'probe.pyo', 'probe.pyd', '.venv/probe', 'node_modules/probe')


def generated_path(name):
    path = PurePosixPath(name)
    return bool(set(path.parts) & IGNORED_DIRS) or path.name == '.DS_Store' or path.suffix in ('.pyc', '.pyo', '.pyd')


def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull, GIT_OPTIONAL_LOCKS='0')
    return env


def git(root, *args, input=None):
    return subprocess.run(['git', '-c', 'core.excludesFile='+os.devnull, '-c', 'core.hooksPath='+os.devnull, '-C', str(root), *args],
                          input=input, capture_output=True, text=True, env=git_env())


def hygiene(root):
    errors, warnings = [], []
    if not (root / '.gitignore').is_file() or (root / '.gitignore').is_symlink():
        return ['A regular root .gitignore is required'], warnings
    try:
        # Include nested rules so negations cannot silently undo root exclusions.
        rules = []
        for directory, folders, files in os.walk(root, followlinks=False):
            folders[:] = [f for f in folders if f not in IGNORED_DIRS | {'.git'} and not (Path(directory)/f).is_symlink()]
            if '.gitignore' in files:
                path = Path(directory)/'.gitignore'
                if path.is_symlink():
                    errors.append('Symlink ignore file: '+str(path.relative_to(root)))
                else:
                    rules.append(path)
        with tempfile.TemporaryDirectory(prefix='zyris-ignore-') as td:
            temp = Path(td)
            result = git(temp, 'init', '--quiet', '--template=')
            if result.returncode:
                raise OSError('Cannot initialize isolated Git ignore check')
            probes = set(PROBES)
            for path in rules:
                relative = path.relative_to(root)
                dest = temp / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(path.read_bytes())
                probes.update(str(relative.parent / p) for p in PROBES)
            probes.update('skills/example/'+p for p in PROBES)
            result = git(temp, 'check-ignore', '--no-index', '--stdin', input='\n'.join(sorted(probes))+'\n')
            if result.returncode not in (0, 1):
                raise OSError('Git ignore evaluation failed')
            missing = probes - set(result.stdout.splitlines())
            if missing:
                errors.append('Required ignore rules ineffective: '+', '.join(sorted(missing)))
        inside = git(root, 'rev-parse', '--is-inside-work-tree')
        if inside.returncode == 0 and inside.stdout.strip() == 'true':
            result = git(root, 'ls-files', '-z', '--cached', '--', '.')
            if result.returncode:
                raise OSError('Cannot inspect tracked paths')
            bad = [p for p in result.stdout.split('\0') if p and generated_path(p)]
            if bad:
                errors.append('Generated/local files are already tracked: '+', '.join(bad))
        else:
            warnings.append('No Git working tree: tracked-file hygiene cannot be checked')
    except (OSError, subprocess.SubprocessError) as exc:
        warnings.append('Git hygiene check incomplete: '+str(exc))
    return errors, warnings


def python_payload(files):
    """Check syntax and obvious imports without importing or executing target code.

    Dynamic imports, host tools and dependency installation require package tests.
    Unresolved imports are warnings, not an invented dependency-install action.
    """
    errors, warnings = [], []
    stdlib = getattr(sys, 'stdlib_module_names', set(sys.builtin_module_names))
    for name, content in files.items():
        if not name.endswith('.py'):
            continue
        try:
            tree = ast.parse(content, filename=name)
        except (SyntaxError, ValueError) as exc:
            errors.append(f'{name}: {exc}')
            continue
        parent = PurePosixPath(name).parent
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                continue
            modules = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or '']
            level = getattr(node, 'level', 0)
            for module in modules:
                first = module.split('.')[0]
                if not level and first in stdlib:
                    continue
                base = parent
                for _ in range(max(0, level-1)):
                    base = base.parent
                if level and not module:
                    # from . import sibling: inspect aliases, rather than certifying an empty module.
                    targets = [a.name for a in node.names]
                else:
                    targets = [module.replace('.', '/')]
                for target in targets:
                    options = [base / target]
                    if not level:
                        options.append(PurePosixPath(target))
                    if not any(str(p)+'.py' in files or str(p/'__init__.py') in files for p in options):
                        warnings.append(f'{name}: import {"."*level}{module or target} is not resolved in the package; verify dependencies and execution context')
    return errors, sorted(set(warnings))
