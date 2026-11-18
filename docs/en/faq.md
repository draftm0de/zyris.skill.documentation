# Faq

[Deutsch](../de/faq.md) | **English**

<img src="../assets/zyris-icon.png" alt="ZYRIS" width="48">

[Start](../../README.en.md) · [Guides](README.md)

## Product and access

The Manager bundles init, update, verify, export and publish. The user confirmed imports from its GitHub repository in Claude and GPT.

## Requirements

Import and use require host account and repository access. Local Python helpers need Python 3.10+. Publish needs GitHub write access and suitable host Git/GitHub tools.

## Privacy and persistence

Exclude private CVs, state, credentials and unrelated work from documentation. Journals belong outside the plugin and source repositories.

## Troubleshooting

**Does `/plugin …` only open settings?** This behavior was observed in the Claude Desktop Code tab. Use the [graphical installation path](installation.md) there. Terminal slash commands do not establish that a desktop installation was performed.

For metadata drift run `make sync-plugin` and review the diff. For a missing update refresh the marketplace and open a new chat. An internal Codex label of 1.0.0 does not mean you must maintain a release version.

## Validation limits

Structural checks and successful import do not prove every feature, automatic updates or an entire publication run. ZIPs and tags are unnecessary for this installation path.
