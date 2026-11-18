# Release and nontechnical installation contract

Use the canonical `templates/plugin/scripts/release.py`, `publish.py` and `tests/test_release.py`. Synchronize consumers; never maintain independent release logic. Root plugin.json owns the numeric base version. Stable tags use vBASE; prereleases use vBASE-alpha.N, beta.N or rc.N. Development builds retain content hashes. Do not promote preview bundles.

Separate source repository, immutable release bundles, installable catalog and public host discovery. Recommend one generated catalog with relative plugin sources for small product families. Generated runtime copies are artifacts, never maintained sources. No new public repository or channel without authorization.

For each selected documentation language, installation must answer prerequisites, surface/OS/account, manager location, address/file, visible steps, permissions, success check, first prompt, updates/removal and common errors. Explain marketplace as plugin catalog. Keep developer commands off the normal user path. Verify current official host instructions and native evidence separately. No final address before approval/publication; label previews. Codex CLI registration is not a GUI claim. Distinguish personal Claude catalogs from restricted organization sync.

Use fictional data and isolated native profiles. Never modify personal installs merely to capture screenshots. Store reviewed captures under docs/assets/LANGUAGE, with host, OS, version, date, provenance, alt text and captions. Otherwise supply a concrete capture checklist without broken images. Preserve configured languages; EN-only and DE-only are valid.

Release acceptance includes conflicts, reproducibility, complete resources, partial failure and retry, generated catalogs, native artifact install/update/remove, preserved private data and recovery. A local test distribution is not a public installation acceptance. Keep explicit gates for screenshots, account restrictions, public channels and rollback limitations.

Publication is orchestrated by the Manager publish capability after explicit approval; no release Action is installed by init. Validation CI remains read-only. Read `publish.md` for the binding approval and recovery workflow. Maintain CHANGELOG.md; release notes derive from its version section. Runtime version remains in plugin.json.
