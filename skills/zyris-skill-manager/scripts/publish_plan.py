#!/usr/bin/env python3
"""Local approval-bound publication journal. Never commits, pushes or publishes.

The hosting agent performs Git/provider operations according to publish.md after
explicit user approval. This file records that approval, not an authentication proof.
"""
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
sys.dont_write_bytecode = True

STAGES = ['prepared', 'approved', 'committed', 'pushed', 'pr_open', 'checks_passed', 'merged']
FIELDS = {'committed': ['commit'], 'pushed': ['commit', 'branch'],
          'pr_open': ['url', 'head'], 'checks_passed': ['head', 'checks'],
          'merged': ['commit', 'url']}


def encoded(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def safe_file(root, name):
    if not isinstance(name, str) or not name or Path(name).is_absolute() or any(p in ('', '.', '..') for p in name.split('/')):
        raise ValueError('Expected a repository-relative file path')
    parts = Path(name).parts
    if any(p in ('.git', '.tmp', 'dist', '.idea', '__pycache__', '.venv', 'node_modules') or p.startswith('.env') for p in parts) or Path(name).suffix in ('.pem', '.key', '.pyc', '.pyo'):
        raise ValueError('Private/generated file cannot be selected: ' + name)
    path = root
    for part in parts:
        path /= part
        if path.is_symlink(): raise ValueError('Symlink cannot be selected: ' + name)
    if path.exists() and not path.is_file(): raise ValueError('Select files, not directories')
    return path


def fingerprint(root, files):
    result = {}
    for name in files:
        path = safe_file(root, name)
        # Ignore checks use Git's effective rules, including local/nested rules.
        ignored = subprocess.run(['git', '-C', str(root), 'check-ignore', '--no-index', '-q', '--', name], capture_output=True)
        if ignored.returncode not in (0, 1): raise ValueError('Cannot check ignore rules')
        if ignored.returncode == 0: raise ValueError('Ignored file cannot be selected: ' + name)
        result[name] = {'sha256': sha(path.read_bytes()), 'executable': bool(path.stat().st_mode & 0o111)} if path.exists() else None
    return result


def stable(root, files):
    origin = git(root, 'remote', 'get-url', 'origin').decode().strip()
    if not (re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', origin)
            or re.fullmatch(r'git@github\.com:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', origin)):
        raise ValueError('Use a credential-free GitHub origin URL; never journal embedded credentials')
    return {'head': git(root, 'rev-parse', 'HEAD').decode().strip(),
            'files': fingerprint(root, files),
            'metadata': fingerprint(root, [p for p in ('plugin.json', '.claude-plugin/plugin.json', '.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json') if (root / p).exists()]),
            'index': sha(git(root, 'diff', '--cached', '--binary', 'HEAD', '--')),
            'origin': origin}


def check_proposal(root, proposal):
    required = {'files', 'commit_message', 'pr_title', 'pr_body',
                'branch', 'base_branch', 'repository', 'merge_method', 'checks'}
    if set(proposal) != required: raise ValueError('Proposal fields must be: ' + ', '.join(sorted(required)))
    if proposal['merge_method'] not in ('squash', 'merge', 'rebase'): raise ValueError('Invalid merge method')
    for field in ('commit_message', 'pr_title', 'pr_body', 'base_branch', 'branch', 'repository'):
        if not isinstance(proposal[field], str) or not proposal[field].strip(): raise ValueError('Missing ' + field)
    for field in ('branch', 'base_branch'):
        subprocess.run(['git', 'check-ref-format', '--branch', proposal[field]], check=True, capture_output=True)
    if not proposal['branch'].startswith('codex/') or proposal['branch'] == proposal['base_branch']:
        raise ValueError('Use a separate codex/ feature branch')
    if not re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', proposal['repository']):
        raise ValueError('This workflow currently supports GitHub repositories only')
    files = proposal['files']
    if not isinstance(files, list) or not files or len(files) != len(set(files)):
        raise ValueError('Select a unique explicit file list')
    manifest = json.loads(safe_file(root, 'plugin.json').read_text())
    if manifest.get('repository') != proposal['repository']:
        raise ValueError('Manifest repository does not match proposal')
    if 'version' in manifest:
        raise ValueError('Repository publication follows commits; omit the manifest version')
    checks = proposal['checks']
    if not isinstance(checks, list) or not checks or any(not isinstance(c, dict) or c.get('result') != 'passed' or not c.get('name') or not c.get('evidence') for c in checks):
        raise ValueError('Record passing checks and their evidence before proposing publication')


def state_directory(path, root=None):
    path = Path(path).expanduser().absolute()
    if any(p.is_symlink() for p in (path, *path.parents)): raise ValueError('State path must not contain symlinks')
    path = path.resolve()
    installation = Path(__file__).resolve().parents[3]
    if path.is_relative_to(installation) or (root and path.is_relative_to(root.resolve())):
        raise ValueError('Publication journal belongs outside the source and plugin installation')
    return path


@contextlib.contextmanager
def locked(path):
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = path / '.lock'
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    try: yield
    finally: lock.unlink()


def write(path, data):
    fd, name = tempfile.mkstemp(prefix='.state-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(encoded(data)); handle.flush(); os.fsync(handle.fileno())
        os.replace(name, path)
    finally: Path(name).unlink(missing_ok=True)


def read(path):
    path = state_directory(path)
    if (path / 'publication.json').is_symlink(): raise ValueError('Journal file must not be a symlink')
    data = json.loads((path / 'publication.json').read_text())
    if data['plan'].get('schema_version') != 2:
        raise ValueError('Legacy publication journal: prepare a new plan and obtain new approval')
    if sha(encoded(data['plan'])) != data['digest']: raise ValueError('Publication plan integrity mismatch')
    if data['stage'] not in STAGES: raise ValueError('Unknown journal stage')
    return data


def prepare(root, proposal, state):
    root = Path(root).resolve(); state = state_directory(state, root)
    check_proposal(root, proposal)
    if git(root, 'diff', '--cached', '--name-only').strip():
        raise ValueError('Existing staged changes: preserve them and prepare in an isolated checkout')
    current = stable(root, proposal['files'])
    origin = current['origin'].removesuffix('.git').replace('git@github.com:', 'https://github.com/')
    if origin != proposal['repository']:
        raise ValueError('Git origin and proposed repository differ')
    # No pre-existing staged changes may be swept into the publication commit.
    plan = {'schema_version': 2, 'source': str(root), 'proposal': proposal, 'snapshot': current}
    data = {'plan': plan, 'digest': sha(encoded(plan)), 'stage': 'prepared', 'events': []}
    with locked(state):
        file = state / 'publication.json'
        if file.exists():
            previous = read(state)
            if previous['digest'] != data['digest']: raise ValueError('Existing plan differs; use a new journal and new approval')
            return previous
        write(file, data)
    return data


def ensure_current(data):
    plan = data['plan']
    if stable(Path(plan['source']), plan['proposal']['files']) != plan['snapshot']:
        raise ValueError('Source changed after preparation; revalidate and obtain new approval')


def approve(state, digest, user_reply, confirmed=False):
    state = state_directory(state)
    if not confirmed: raise ValueError('All listed actions must be explicitly confirmed by the user')
    if not user_reply.strip(): raise ValueError('Explicit user reply is required; never synthesize consent')
    with locked(state):
        data = read(state)
        if digest != data['digest']: raise ValueError('Approval is for a different plan')
        if data['stage'] != 'prepared':
            if data['events'] and data['events'][0].get('user_reply') == user_reply: return data
            raise ValueError('Already approved with a different reply')
        ensure_current(data)
        data['stage'] = 'approved';data['events'].append({'stage': 'approved', 'digest': digest, 'user_reply': user_reply})
        write(state / 'publication.json', data)
    return data


def checkpoint(state, stage, evidence):
    state = state_directory(state)
    with locked(state):
        data = read(state)
        if data['stage'] == stage and data['events'][-1].get('evidence') == evidence: return data
        if stage not in FIELDS or STAGES.index(stage) != STAGES.index(data['stage']) + 1:
            raise ValueError('Cannot skip approval or publication stages')
        if not isinstance(evidence, dict) or any(not evidence.get(f) for f in FIELDS[stage]):
            raise ValueError('Missing checkpoint evidence')
        proposal = data['plan']['proposal']
        for field in ('commit', 'head'):
            if field in evidence and not re.fullmatch(r'(?:[0-9a-f]{40}|[0-9a-f]{64})', str(evidence[field])):
                raise ValueError('Checkpoint requires a full commit hash')
        if 'url' in evidence:
            repository = proposal['repository']
            if not isinstance(evidence['url'], str) or not re.fullmatch(re.escape(repository) + r'/pull/[1-9][0-9]*', evidence['url']):
                raise ValueError('Checkpoint URL belongs to another repository')
        events = {event['stage']: event.get('evidence', {}) for event in data['events']}
        if stage == 'pushed' and (evidence['commit'] != events['committed']['commit'] or evidence['branch'] != proposal['branch']):
            raise ValueError('Pushed commit/branch differs from approved publication')
        if stage in ('pr_open', 'checks_passed') and evidence['head'] != events['committed']['commit']:
            raise ValueError('PR head changed; new review required')
        if stage == 'checks_passed' and (not isinstance(evidence['checks'], list) or not evidence['checks'] or any(not isinstance(c, dict) or not c.get('name') or c.get('result') != 'passed' for c in evidence['checks'])):
            raise ValueError('Pending/failed checks must not be bypassed')
        if stage == 'merged' and evidence['url'] != events['pr_open']['url']:
            raise ValueError('Merged PR differs from approved publication')
        data['stage'] = stage;data['events'].append({'stage': stage, 'evidence': evidence})
        write(state / 'publication.json', data)
    return data


def main():
    p = argparse.ArgumentParser(description=__doc__); sub = p.add_subparsers(dest='command', required=True)
    a = sub.add_parser('prepare');a.add_argument('--source', required=True);a.add_argument('--proposal', required=True);a.add_argument('--state-dir', required=True)
    a = sub.add_parser('approve');a.add_argument('--state-dir', required=True);a.add_argument('--digest', required=True);a.add_argument('--reply-file', required=True);a.add_argument('--confirm-all-actions', action='store_true')
    a = sub.add_parser('checkpoint');a.add_argument('--state-dir', required=True);a.add_argument('--stage', required=True, choices=list(FIELDS));a.add_argument('--evidence', required=True)
    for command in ('status', 'check-before-commit'):
        a = sub.add_parser(command);a.add_argument('--state-dir', required=True)
    args = p.parse_args()
    try:
        if args.command == 'prepare': data = prepare(args.source, json.loads(Path(args.proposal).read_text()), args.state_dir)
        elif args.command == 'approve': data = approve(args.state_dir, args.digest, Path(args.reply_file).read_text(), args.confirm_all_actions)
        elif args.command == 'checkpoint': data = checkpoint(args.state_dir, args.stage, json.loads(Path(args.evidence).read_text()))
        else:
            data = read(args.state_dir)
            if args.command == 'check-before-commit':
                if data['stage'] != 'approved': raise ValueError('Explicit approval required')
                ensure_current(data)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        p.exit(1, str(exc) + '\n')

if __name__ == '__main__': main()
