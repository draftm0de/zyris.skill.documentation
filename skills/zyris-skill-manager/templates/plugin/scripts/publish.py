#!/usr/bin/env python3
"""Explicit GitHub release publication; identical retries resume without clobber."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
sys.dont_write_bytecode = True
import release


def gh(*args):
    return subprocess.check_output(['gh', *args], text=True)


def publish(bundle, repository):
    bundle = Path(bundle)
    record = release.verify_bundle(bundle)
    if record['repository'] != 'https://github.com/' + repository:
        raise ValueError('Repository does not match release provenance')
    tag = record['tag']
    # Confirm immutable remote tag before any mutation; gh does not create tags for us.
    remote = json.loads(gh('api', f'repos/{repository}/commits/{tag}'))
    if remote['sha'] != record['commit']:
        raise ValueError('Remote tag differs from release commit')
    # Listing errors must propagate, never be interpreted as a missing release.
    releases = json.loads(gh('api', '--paginate', '--slurp', f'repos/{repository}/releases?per_page=100'))
    existing = next((r for page in releases for r in page if r['tag_name'] == tag), None)
    notes = (bundle / 'release-notes.md').read_text()
    if existing is None:
        gh('release', 'create', tag, '--repo', repository, '--verify-tag', '--draft', '--title', tag, '--notes-file', str(bundle / 'release-notes.md'))
    elif existing['body'].replace('\r\n', '\n') != notes.replace('\r\n', '\n'):
        raise ValueError('Existing release notes differ')
    data = json.loads(gh('release', 'view', tag, '--repo', repository, '--json', 'assets,isDraft'))
    local = release.snapshot(bundle)
    names = [a['name'] for a in data['assets']]
    if len(names) != len(set(names)) or set(names) - set(local):
        raise ValueError('Unexpected remote assets')
    with tempfile.TemporaryDirectory() as directory:
        if names:
            gh('release', 'download', tag, '--repo', repository, '--dir', directory)
        for name in names:
            if (Path(directory) / name).read_bytes() != local[name]:
                raise ValueError('Published asset conflict: ' + name)
    missing = sorted(set(local) - set(names))
    if not data['isDraft'] and missing:
        raise ValueError('Cannot repair a published release; publish a new version')
    for name in missing:
        gh('release', 'upload', tag, str(bundle / name), '--repo', repository)
    # Resume after upload failure by rerunning; existing bytes are compared first.
    if data['isDraft']:
        gh('release', 'edit', tag, '--repo', repository, '--draft=false', '--prerelease=' + str('-' in record['version']).lower(), '--latest=false')
    return {'published': True, 'tag': tag}

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle', required=True); p.add_argument('--repository', required=True)
    p.add_argument('--publish', action='store_true', required=True)
    a = p.parse_args()
    try: print(json.dumps(publish(a.bundle, a.repository)))
    except (ValueError, OSError, subprocess.CalledProcessError) as e: p.exit(1, str(e) + '\n')
