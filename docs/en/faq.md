# FAQ

[Deutsch](../de/faq.md) | **English**

[Home](../../README.en.md) · [Overview](README.md) · [Install](installation.md) · [Use](usage.md) · [Screens](screens.md) · [FAQ](faq.md)

## Product and access

The product is a plugin containing skills and Claude commands. It builds GitHub Markdown, not a store or protected distribution platform. It does not commit, push or publish without instruction.

## Requirements

The host needs access to source and an execution environment for the Python helpers. Local packaging needs Python 3.10+ and Make; Claude installation also needs its CLI. Without suitable tools, automated checks remain pending.

## Privacy and persistence

There is no dedicated database service. Documentation and the source locator live in the target project. Private CVs, session data, `.env` and credentials are not documentation sources.

## Troubleshooting

If multiple skills are found, specify the exact skill folder. For an existing destination use `verify` and targeted edits. If an existing logo differs, the user decides how to handle it; the helper does not silently overwrite it.

## Validation limits

The structure audit does not execute target code and is not a comprehensive secret scanner. Documentation validation checks pages, links, headings, language switches and placeholders; factual accuracy and translation quality require semantic review as well.

---

Documentation prepared with ZYRIS Skill Documentation. Source-product ownership remains unchanged.
