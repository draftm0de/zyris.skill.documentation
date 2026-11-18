# Storage and recovery

[Deutsch](../de/storage.md) | **English**

[Home](../../README.en.md) · [Overview](README.md) · [Install](installation.md) · [Use](usage.md) · [Screens](screens.md) · [FAQ](faq.md)

## Storage model

Files in the target repository are the output. `README.md` and `docs/de/` are German; `README.en.md` and `docs/en/` are English. The shared logo is at `docs/assets/zyris-icon.png`.

## Setup and configuration

The optional locator contains `schema_version`, optional `source_skill`, `extra_sources`, `open_questions` and the `documentation` language configuration. Relative sources must stay within the repository. External sources store documentation settings without a source pointer; supply the source again on the next invocation.

## Save and resume

Changes are saved as ordinary files. On resumption the agent rereads canonical source. Resolved questions are removed or clarified in the authoritative source file; product descriptions are not duplicated in the manifest.

## Failures and recovery

Scaffolding does not overwrite existing pages. `init` refuses populated destinations. Write failures may leave already created files; review the diff and resume deliberately. Project-wide transactions and concurrent multi-agent writes are not guaranteed.

## Limitations

No automatic cloud synchronization, persistent chat memory or backup service. Use the target project’s version control. A commit remains a separately authorized action.

---

Documentation prepared with ZYRIS Skill Manager. Source-product ownership remains unchanged.

### Publish journal

The private approval journal lives outside the plugin installation and source repository. It contains selected paths/hashes, proposed messages, the approval reply and publication evidence. Never store tokens; retain it for recovery and delete it only when requested. See [publish](publish.md).
