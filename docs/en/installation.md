# Installation and updates

[Deutsch](../de/installation.md) | **English**

[Home](../../README.en.md) · [Overview](README.md) · [Install](installation.md) · [Use](usage.md) · [Screens](screens.md) · [FAQ](faq.md)

## Choose your platform

Claude Code uses a local plugin marketplace. ChatGPT receives a plugin ZIP; upload availability depends on account and workspace permissions. This is not a standalone skill installation.

## Install

For Codex: `make install TARGET=codex` or `bash install.sh install --target codex`. The build generates native `.codex-plugin/plugin.json` metadata and a local Codex marketplace. The installer registers it with `codex plugin marketplace add` and installs using `codex plugin add`. Requires a Codex CLI supporting these commands; tested with 0.165.0. Then open a new Codex chat; restart Codex if needed.

```sh
make install TARGET=claude
```

Alternatively: `bash install.sh install --target claude`. Preview with `make install TARGET=claude DRY_RUN=1`. For ChatGPT run `make package`, then upload `dist/zyris-skill-documentation-chatgpt-plugin.zip` in plugin administration. Enable the plugin in the host.

## Update

Codex: `make update TARGET=codex` rebuilds, re-registers the same local marketplace and installs the new content version. Keep the repository folder accessible. No standalone skills are copied and installations from other marketplaces are not removed.

Without Make: `bash install.sh update --target claude`. Both commands use the same implementation.

After changes run `make update TARGET=claude`, then restart Claude Code. Install the local marketplace once before updating. `make update TARGET=chatgpt` rebuilds the package; upload the new version manually. Content changes produce a new package version.

## Remove

Remove the plugin through the host’s plugin management. Generated documentation in target repositories remains in place.

## Verify first use

Run `verify` on a fictional test project. Confirm the report identifies the source, changes nothing and lists pending acceptance checks. Package validation does not replace this host test.

---

Documentation prepared with ZYRIS Skill Documentation. Source-product ownership remains unchanged.
