# Release verification evidence

## Current status: Skill Manager

2026-11-18: local Manager rename and publish capability implemented. Manager: 86 tests, 85 passed and one optional test skipped. Interview Coach: 97 tests, 96 passed and one optional test skipped. These include 18 new publish tests covering explicit approval, version/file conflicts, preservation of unrelated work, journal locks, resumption and extracted-package execution. Test commits occur only in disposable fictional repositories; none were created in the product repositories.

Verify: 35 Manager and 25 Coach checks without warnings. Packaging, documentation validation and website export passed. The renamed Manager and Coach were installed in isolated Claude Code/Codex profiles, updated with changed skill contents, restored to original contents under a higher test version and removed; fictional private data survived.

The journal helper does not execute Git/GitHub publication. Publication is a host-agent workflow with explicit approval and verified intermediate states. No live remote commit/push/PR/merge/release/catalog run was performed; remote orchestration is not production-accepted. The public GitHub address remains unchanged. Previous generated Documentation artifacts were preserved under `.tmp/pre-manager-dist/`; active installations were not changed.

## Historical baseline before the Manager migration

2026-11-18 · macOS · Claude Code 2.1.319 · Codex CLI 0.165.0.

Local test distribution, not a public release. Available desktop applications use the personal profile; no isolated GUI test account was established and those installations were not changed.

| Check | Result |
|---|---|
| Coach unit + regression | 95 tests, 1 optional native test skipped |
| Documentation | 66 tests, 1 optional native test skipped |
| Release contract | 12 tests per repository, included above: versions/tags, clean commit, deterministic retry, corruption, locks, failed atomic write, partial upload, catalog completeness |
| Native CLI / both products | Install A (0.1.0), runtime update to fictional B (0.1.1), forward recovery C (0.1.2), uninstall: passed in both hosts |
| Private fixture | Separate fictional progress file preserved byte-for-byte |
| Extracted runtime | Existing package lifecycle/initialization regression tests passed |
| GUI / screenshots / model conversation | User screenshots establish German Claude Desktop navigation through repository selection; sync/install and model conversation remain unverified |
| Public catalog / public release | Not published; final acceptance pending |

The native run used temporary HOME, CODEX_HOME and CLAUDE_CONFIG_DIR directories, the generated combined catalog and a working directory outside both source checkouts. Test version 0.1.1 changed skill files; 0.1.2 restored their original bytes. Installed or host-loaded skill resources were compared byte-for-byte with the catalog. No model was invoked or private data read. Local run logs remain in the task’s ignored scratch directory; no private raw logs are exported.

A real public Git catalog, account entitlement, graphical updates and downgrades remain open. Atomic local retry recovery is tested; native downgrade behavior was not established. Safe operating strategy: higher patch release with known-good runtime. Pending captures: [examples](screens.md). Workflow and approvals: [release operations](release-operations.md).

Additional checks: documentation validation, packaging and website export passed; Verify 34 checks without warnings. Graphical app versions read from app metadata only: ChatGPT/Codex 26.1111.21308 (27194), Claude Desktop 5.11492.5. This is not UI acceptance.

Repeat the native check (isolated profiles, both CLIs required):

```sh
python3 -B scripts/test_release_native.py --bundle dist/release-preview-final --output .tmp/native-release.json
```

Update: user captures dated 2026-11-18 establish the German Claude Desktop path up to repository entry. Two dialog images are included on the [examples page](screens.md). They do not establish synchronization or product installation.

Codex UI update: the user reports **User Icon → Settings → Integration → Plugins → + Add → A Marketplace**. This supplies a graphical entry path; subsequent dialog, catalog import and plugin installation are not confirmed by screenshots or an independent run.
