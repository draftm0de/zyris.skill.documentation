# Usage

[Deutsch](../de/usage.md) | **English**

[Home](../../README.en.md) · [Overview](README.md) · [Install](installation.md) · [Use](usage.md) · [Screens](screens.md) · [FAQ](faq.md)

## Set up

Choose languages per target repository: German only, English only or both. In `docs/documentation.json`, `documentation` can contain `{"languages":["en"],"default_language":"en"}`. English only produces `README.md` and `docs/en/`; German pages and language switches are not required. The agent asks when the choice is unclear. Switching languages does not automatically delete existing content.

Provide a local skill or repository path. Multiple skills require a selection. Without local filesystem access, provide a sanitized source archive. A path on your computer does not automatically become available in a cloud session.

## Choose a workflow

In Codex select the installed plugin or request it by name: “Use ZYRIS Skill Manager to verify this repository.” The plugin bundles init, update and verify capabilities; Claude slash commands are not assumed to apply to Codex.

In Claude:

```text
/zyris-skill-manager:verify ../my-plugin
/zyris-skill-manager:update ../my-plugin
/zyris-skill-manager:init ../my-skill ../new-plugin
```

In ChatGPT: “Use ZYRIS Skill Manager to verify this plugin’s structure.” or “Update its German and English documentation.”

## Understand the output

The structure report distinguishes failures, warnings and manual checks. `production_ready: null` explicitly means not established. `init` initially creates templates; the agent must then author their content from source evidence.

## Control the session

The agent asks about contradictions. You can limit scope or stop work. Changes occur in individual files; stopping does not guarantee an automatic rollback. Review the Git diff.

## Return later

Run `update` again. `docs/documentation.json` can locate the canonical skill and additional sources. It does not store facts, versions or capabilities; those are reread from source.

## Specialized workflows

[**publish: prepare and approve publication**](publish.md). Review the proposed version and commit message before commit/push/PR/merge. Tag, release and catalog promotion follow within the same approved scope.


The `export` action validates or builds a website bundle from existing source. In Claude: `/zyris-skill-manager:export REPOSITORY`. In Codex or ChatGPT request the documentation export from the plugin. Exporting does not publish or rewrite content.

`init` requires a separate empty destination; `.git`, `.idea` and `.DS_Store` may exist. Existing projects are audited first and changed deliberately. The original source is not moved. The new project receives an independent copy, not automatic synchronization.

---

Documentation prepared with ZYRIS Skill Manager. Source-product ownership remains unchanged.
