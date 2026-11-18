# Usage

[Deutsch](../de/usage.md) | **English**

<img src="../assets/zyris-icon.png" alt="ZYRIS" width="48">

[Start](../../README.en.md) · [Guides](README.md)

## Set up

Provide an accessible source folder. Language and output are resolved per repository; `docs/documentation.json` stores only source pointers, languages and export configuration. A hosted session without local access needs a sanitized source copy.

## Choose a workflow

Choose init, update, verify, export or publish. For example, in Claude Code use `/zyris-skill-manager:init SOURCE OUTPUT`. In Codex/GPT select the relevant capability or describe the action. Claude slash-command UI is not assumed for every host.

## Understand the output

Init creates a separate copy under `skills/`, a versionless manifest, both marketplace files, the Claude manifest and development/documentation starters. Missing repository URL and publisher metadata must be resolved. Templates alone are not finished product documentation. Verify distinguishes failures, warnings and outstanding manual checks; `production_ready: null` is not approval.

## Control the session

Limit the request to the intended files or actions. Init never overwrites an existing project. Existing projects receive targeted edits; review their diff. Stopping does not automatically undo completed changes.

## Return later

Update reads current sources again. Publish can resume from a private journal after checking actual GitHub state and the original approval. Old release journals require a new plan.

## Specialized workflows

[Publish](publish.md) proposes a commit message and performs commit → push → PR → checks → merge only after approval. No version approval, tags or releases. Export creates a website ZIP from existing Markdown; that ZIP is not an installation package.
