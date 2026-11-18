# ZYRIS Skill Manager

[Deutsch](README.md) | **English**

This plugin documents accessible local skills and plugins from source evidence. Documentation languages are chosen per repository: German only, English only or both. Use `init` for a separate empty plugin starter, `update` to refresh documentation, or `verify` for a read-only structure audit. The agent asks about material uncertainties. Passing structural checks does not establish production readiness. Nothing is published or installed without instruction.

In Claude: `/zyris-skill-manager:verify SOURCE_PATH`, with equivalent `:init` and `:update` commands. In ChatGPT request the action in natural language. The host must have access to the source; helpers require Python 3.10 or newer.

[Workflow and limitations](skills/zyris-skill-manager/SKILL.md)

## Publish with approval

`/zyris-skill-manager:publish SOURCE` prepares the version, CHANGELOG.md, commit message, PR text, checks and destinations. Only after explicit combined approval does the host execute commit, push, PR, merge, tag, release and catalog promotion. No release Action is required. The bundled journal helper supports resumption and detects changed contents; it does not publish itself. The specified provider workflow currently supports GitHub. [Workflow](skills/zyris-skill-manager/references/publish.md).
