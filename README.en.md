# ZYRIS Skill Manager

[Deutsch](README.md) | **English**

<img src="docs/assets/zyris-icon.png" alt="ZYRIS" width="48">

## Who it is for

For developers and teams maintaining skills as installable plugins. The Manager supports structure, documentation, validation, website export and publication through a checked GitHub PR.

## What it looks like

One plugin with six skill entry points. [Example and real Claude dialogs](docs/en/screens.md) show the workflow. The user confirmed repository imports in Claude and GPT on 2026-11-18.

## Capabilities and modes

**init** creates a separate plugin skeleton. **update** maintains documentation from source evidence. **verify** checks structure and metadata. **export** creates the website documentation bundle. **publish** proposes a commit message and performs commit, push, PR and merge after approval. [Publication details](docs/en/publish.md).

## Quick start

Add `https://github.com/draftm0de/zyris.skill.manager` as a marketplace in plugin settings and install **ZYRIS Skill Manager**. No ZIP or tag is needed. [Installation paths](docs/en/installation.md).

## Usage

Select the plugin and ask: “Verify this repository.” For documentation: “Update the documentation in German and English.” Claude Code also supports `/zyris-skill-manager:verify PATH` and the other action commands. [Usage](docs/en/usage.md).

## Storage and privacy

The Manager writes documentation and, for init, a separate source copy. Publication journals stay outside the source and plugin installation. Private data, credentials and unrelated changes are excluded. Your AI host processes supplied sources under its own terms.

## Project status

The user confirmed repository imports in Claude and GPT. CLI imports were also tested in isolated profiles. This does not certify every feature, automatic updates or the entire publication workflow. License: [MIT](LICENSE). [Evidence](docs/en/release-evidence.md).

## Development

```sh
make sync-plugin
make check-plugin
make test
make verify SOURCE=.
make validate-docs OUTPUT=.
make check-docs-export
```

`make sync-plugin` generates host metadata to commit. `make update TARGET=codex` refreshes the installed remote copy; the **update** skill action maintains documentation. [Development](docs/en/development.md).
