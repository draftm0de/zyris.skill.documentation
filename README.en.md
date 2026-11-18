# ZYRIS Skill Documentation

[Deutsch](README.md) | **English**

<img src="docs/assets/zyris-icon.png" alt="ZYRIS" width="48">

[Documentation](docs/en/README.md) · [Screens](docs/en/screens.md)

A plugin for consistent documentation in repository-selected languages and evidence-based structure checks of skills and plugins.

## Who it is for

For developers and teams distributing skills as plugins and maintaining practical GitHub documentation. The plugin inspects accessible source folders and asks about material uncertainties.

## What it looks like

This repository uses German and English with German as the default. Other target repositories can choose German, English or both. [Walkthrough and screens](docs/en/screens.md) illustrate usage with an explicitly fictional example. Actual host screenshots are pending.

## Capabilities and modes

**init** creates a separate plugin starter from a skill. **update** refreshes documentation from current sources. **verify** checks structure and identifies unresolved release gates. Folder checks alone do not establish production readiness.

## Quick start

Requires Python 3.10 or newer, Make, and Claude Code for native installation.

```sh
make test
make package
make install TARGET=claude
```

Upload the ChatGPT plugin ZIP manually. See [installation](docs/en/installation.md).

## Usage

In Claude: `/zyris-skill-documentation:verify ../my-plugin`. For documentation: `/zyris-skill-documentation:update ../my-plugin`. In ChatGPT select the plugin and request the action in natural language; the source folder must be accessible to the host.

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

Documentation prepared with ZYRIS Skill Documentation. Source-product ownership remains unchanged.
