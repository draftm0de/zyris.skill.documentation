# Repository publication

The product repository is also its marketplace. `make sync-plugin` derives host files from `plugin.json`; `make check-plugin` validates them. Commit derived files together with the source. Versions, tags, plugin ZIPs, GitHub Releases and a separate catalog repository are unnecessary.

Publish prepares a checked diff and commit message. Approval covers commit, push, PR, required checks/reviews and merge. Corrections use new reviewed commits. No force-push or bypassing branch protections.

User updates are a separate step: sync the marketplace and open a new chat. A successful merge does not prove automatic refresh of every installation. Optional developer archives and website export ZIPs remain separate tools.

[Publish](publish.md) · [Installation](installation.md)
