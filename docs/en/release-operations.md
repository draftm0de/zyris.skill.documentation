# Release operations

## Ownership

ZYRIS Skill Manager orchestrates publication during the active session. No release Action or background service is required; ordinary validation CI remains. Implementing, inspecting or preparing publication does not authorize publishing.

## Version and changelog

`plugin.json` owns the current product version. `CHANGELOG.md` records history with `## [X.Y.Z]`, changes, limitations and upgrade notes. Release notes derive from that section; do not maintain separate docs/releases files. Publish currently targets stable SemVer; development builds retain content hashes and the separate builder supports prereleases.

## Workflow

1. Inspect changes and remote release state; select explicit files and preserve unrelated work.
2. Prepare version, changelog, commit message, PR title/body and destinations. Run tests, Verify, documentation validation, packaging and export.
3. Show the concrete proposal including catalog destination. Request one approval for commit, push, PR, merge, tag, release and catalog promotion. Apply requested changes before approval; silence is not consent.
4. After approval, commit on the feature branch, push and create the PR. Wait for passing checks and required reviews; never bypass protection.
5. Inspect and tag the actual merged commit. Build the strict bundle from it, publish it and promote the complete catalog through the approved route.

Already approved steps need no repeated confirmation. Changed contents, versions, messages or destinations require a new proposal. Approval of only a commit or PR does not authorize the full workflow.

## Tools

The Manager's publish capability executes using Git and GitHub tools. Bundled `publish_plan.py` creates and validates a local approval plan and journals observed progress; it does not itself publish. Store the journal privately outside source repositories and plugin installations. It records file hashes, version, messages, approval reply and commit/PR/release evidence, never credentials. A journal cannot replace actual consent in the conversation.

Shared `scripts/release.py`, `scripts/publish.py` and `scripts/test_release_native.py` remain canonical build/release tools. Invoke the low-level publisher only inside the approved workflow. Local preparation example:

```sh
make test check-plugin check-docs-export export-docs
python3 -B scripts/release.py prepare --tag v0.1.0 --preview --output dist/manager-preview
```

Strict bundles require a clean checkout and a tag at HEAD. Previews are labeled and rejected by normal publication. ZIPs, SHA256SUMS and release.json are deterministic; identical retries succeed, differing outputs are never overwritten. Compression-library differences can affect bytes; reuse the same toolchain for retries.

## Catalog and repository addresses

Source repositories, release bundles, installable catalogs and public host-directory listings are separate. Existing product URLs do not yet contain installable catalogs. A shared generated catalog remains a proposal; generated distribution branches are an alternative. Publish never creates a new repository implicitly. Resolve the existing catalog destination, branch, expected commit and complete product set before approval. Host support for the selected route still needs verification.

One product remains one plugin. Generated manifests and catalog runtime copies are artifacts, never separately maintained sources. provenance.json records release commits and checksums. Review the full desired product set in catalog promotion so other plugins are preserved.

## Recovery

After interruption, reconcile the journal with actual Git/GitHub state before retrying. Do not duplicate commits, PRs or releases after uncertain timeouts. Identical existing tags/assets can be reused; differing ones must never be overwritten. Failed checks block merging. Required independent reviews cannot be replaced by the plugin. A published release with failed catalog promotion is partially completed, not successful publication.

Local journal locks do not protect against remote writers. Check expected commits before every mutation; no force pushes, moved tags or admin bypass. A changed catalog requires a new reviewed proposal. Remove a stale lock only after confirming its writer is gone.

Recover faulty releases with a higher patch containing known-good runtime. A catalog revert does not guarantee cache downgrade. Preserve private data separately and test recovery in isolated profiles.

## Limits and evidence

The specified workflow currently supports GitHub; GitLab MR/release automation is not implemented. Authenticated tools, sufficient permissions and an existing catalog destination are required; the plugin does not grant itself access. It runs during the active session and resumes from the journal after interruption.

[Verification evidence](release-evidence.md). Local tests do not establish live publication, public installation, account access or complete GUI acceptance. No commits, tags, pushes, remote rename or publication were performed during implementation. www.draftmode remains untouched.
