# Storage

[Deutsch](../de/storage.md) | **English**

<img src="../assets/zyris-icon.png" alt="ZYRIS" width="48">

[Start](../../README.en.md) · [Guides](README.md)

## Storage model

Documentation lives in the target repository; init creates a separate source copy. A publication journal stays private outside source and installation.

## Setup and configuration

`docs/documentation.json` stores source pointers and language; `plugin.json` contains product metadata. Derived host files are committed. Temporary files and `dist/` are ignored.

## Save and resume

Git records changes. The journal helper stores the plan digest, approval text and observed stages. It never performs external operations itself.

## Failures and recovery

After interruption inspect actual Git/PR state first. Do not duplicate commits or PRs after a timeout. Changed proposals need renewed approval.

## Limitations

The journal is not identity proof and cannot replace genuine user consent. Uninstalling does not delete external project files. The AI host may process supplied sources.
