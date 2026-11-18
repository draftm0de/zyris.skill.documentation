# ZYRIS Skill Manager

[Deutsch](README.md) | **English**

<img src="docs/assets/zyris-icon.png" alt="ZYRIS" width="48">

[Documentation](docs/en/README.md) · [Screens](docs/en/screens.md)

One plugin for structure, documentation, validation and approval-gated publication of skill plugins.

**Installation preview:** [Claude](docs/en/installation.md#claude-graphical-interface) · [Claude Code](docs/en/installation.md#claude-code) · [Codex Desktop](docs/en/installation.md#codex-desktop). Public catalog address and UI acceptance are pending.

## Who it is for

For developers and teams distributing skills as plugins and maintaining practical GitHub documentation. The plugin inspects accessible source folders and asks about material uncertainties.

## What it looks like

This repository uses German and English with German as the default. Other target repositories can choose German, English or both. [Walkthrough and screens](docs/en/screens.md) illustrate usage with an explicitly fictional example. Claude Desktop dialog screenshots are available; complete installation and publish acceptance remain pending.

## Capabilities and modes

**publish** prepares version, changelog, commit and PR, then performs publication only after your explicit combined approval. [Workflow and limits](docs/en/publish.md). **export** builds the documentation bundle.


**init** creates a separate plugin starter from a skill. **update** refreshes documentation from current sources. **verify** checks structure and identifies unresolved release gates. Folder checks alone do not establish production readiness.

## Quick start

Open the [installation guide](docs/en/installation.md) and choose Claude or Codex. The public catalog address is not approved yet; instructions are a preview. After installation, select the plugin in a new chat and send the documented first prompt. This user path does not require a source checkout.

## Usage

In Claude: `/zyris-skill-manager:verify ../my-plugin`. For documentation: `/zyris-skill-manager:update ../my-plugin`. In ChatGPT select the plugin and request the action in natural language; the source folder must be accessible to the host.

## Storage and privacy

The plugin writes Markdown, public documentation assets and an optional source locator. It needs no dedicated server. Source supplied to an AI host is subject to that host’s processing. Private runtime data and credentials do not belong in documentation.

## Project status

MVP with deterministic tests, three plugin package formats and a structure audit. Native installation, updates and semantic journeys in both hosts remain separate acceptance checks. No publication or full production approval is claimed. License: [MIT](LICENSE).

## Development

Website export from the same sources: `make check-docs-export` and `make export-docs`. See the [development guide](docs/en/development.md).

```sh
make test
make package
make validate-docs OUTPUT=.
make update TARGET=claude
```

`make update` updates the installed documentation plugin. The plugin’s `update` action refreshes a target project’s documentation. See [development](docs/en/development.md) for sources and packaging.

---

Documentation prepared with ZYRIS Skill Manager. Source-product ownership remains unchanged.

Local rename: `zyris.skill.documentation` → `zyris.skill.manager`; plugin ID: `zyris-skill-manager`. GitHub retains its existing address until a separately approved remote rename. Existing installations are not automatically changed.
