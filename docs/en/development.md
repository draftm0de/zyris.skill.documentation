# Development

[Deutsch](../de/development.md) | **English**

[Home](../../README.en.md) · [Overview](README.md) · [Install](installation.md) · [Use](usage.md) · [Screens](screens.md) · [FAQ](faq.md)

## Source of truth

The [main workflow](../../skills/zyris-skill-documentation/SKILL.md) and its references define behavior. Thin action skills delegate to it. `plugin.json` holds the base version; the build derives host manifests. Documentation and its copied logo are derived output.

## Checks

`ZYRIS_TEST_CODEX_NATIVE=1 make test` additionally runs the real Codex CLI in an isolated temporary profile: installation, reinstallation and an update after content changes. This test does not modify the personal Codex profile.

```sh
make test
make validate-docs OUTPUT=.
make verify SOURCE=.
```

`verify` returns exit code 1 for failures or warnings. Missing licensing decisions or unfinished documentation remain visible; do not weaken checks to hide them. Actual host journeys are also required.

## Packaging

The canonical installation implementation lives in `skills/zyris-skill-documentation/templates/plugin/`. Each project’s `scripts/plugin.py`, `install.sh` and `plugin.mk` are generated copies; `verify` detects drift. Name, base version and metadata come from `plugin.json`. The `io.zyris.distribution` extension defines `skillRoot`, optional `marketplace` and optional extra package files (`files`: destination → source). All host manifests are derived during the build.

`make package` builds reproducible Claude, ChatGPT and Codex plugin ZIPs and local Claude and Codex marketplaces in `dist/`. Source symlinks are rejected. Runtime, templates and icon determine the version hash; development files are excluded.

## CI and releases

The [CI](../../.github/workflows/validate.yml) runs tests, packaging and documentation validation. It publishes nothing. A successful local run proves neither remote CI success nor host acceptance.

## Maintain documentation

### Website export

`make check-docs-export` validates the contract; `make export-docs` creates `dist/<plugin-name>-documentation.zip` with `index.json`, unchanged Markdown pages and selected assets. The `export` configuration in `docs/documentation.json` contains only page and asset pointers. Product metadata comes from `plugin.json`; languages come from the existing documentation settings. The index adds link mappings, checksums and Git provenance, explicitly marking local changes. The website owns routing and safe rendering. Nothing is published.

[Export contract v1](../../skills/zyris-skill-documentation/references/export-contract.md)

Run the plugin’s `update` action and review the Git diff for both languages. Use `make scaffold SOURCE=... OUTPUT=...` only for missing templates; the helper does not author prose. `make init-plugin SOURCE=... OUTPUT=...` creates a separate starter with manifests, build, starter tests, CI and documentation templates.

---

Documentation prepared with ZYRIS Skill Documentation. Source-product ownership remains unchanged.

For new projects: `make init-plugin SOURCE=... OUTPUT=... LANGUAGES=en DEFAULT_LANGUAGE=en`. `make scaffold` accepts the same language parameters; conflicting existing configuration is protected.
