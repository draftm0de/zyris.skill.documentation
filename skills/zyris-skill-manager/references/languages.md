# Repository language policy

## Selection and layout

Documentation languages are a repository decision, not a plugin-wide bilingual requirement. Before creating docs, honor the user's choice or read `docs/documentation.json`. If neither determines the languages, ask once. Store only the settings under `documentation`, for example:

```json
{"languages": ["en"], "default_language": "en"}
```

English only: `README.md` and `docs/en/`. German only: `README.md` and `docs/de/`. Bilingual: the chosen default owns `README.md`; the other uses `README.de.md` or `README.en.md`. All guides keep their names under `docs/<language>/`. Counterpart links are required only with both languages. No language switch or missing-language warning for intentionally monolingual repositories.

For backward compatibility, existing manifests without these settings and an existing README.en.md plus docs/de/ and docs/en/ use the former German-default DE/EN layout. New scaffolds require explicit language selection before creating files. The agent must still resolve and record the project decision before new documentation work. CLI flags for a new project: `--languages en --default-language en`, `--languages de`, or `--languages de en --default-language de`. Existing settings take precedence; conflicting CLI flags fail rather than silently rewriting policy. Edit policy deliberately before a language migration; preserve existing content until a reviewed move/removal is authorized.

## Tone and translation

German uses friendly, professional “du”, clear verbs and concise sentences. English uses “you” with the same direct, practical tone. Avoid exaggerated claims and awkward literal translation. Prefer “Einrichtung”, “Nutzung”, “Datenschutz”, “Wiederaufnahme” and “Fehlerbehebung” in German; keep recognizable technical identifiers where needed.

Translate every material capability, limitation, requirement and verification caveat. Do not add a feature or stronger promise in one language. When bilingual, update both versions in the same change.

## Images and examples

For generated diagrams or transcript illustrations, create fully localized variants only for selected languages under `docs/assets/<language>/`; keep the same layout when bilingual. Translate labels, titles, body text, badges, notes and disclaimers. Do not leave German answers inside an otherwise English graphic, or English UI-style headings inside a German graphic. The shared brand icon is language-neutral.

For actual screenshots, retain the real interface language and include a localized caption specifying that language, host and capture date. For bilingual projects, prefer capturing both locales when possible; do not invent translated screenshot UI.

For authentic test excerpts, publish the original in its language. The other version can use an explicitly labelled translation, linked to the original example. Never imply that a translated excerpt was produced by a model in that language. Mark fictional/illustrative examples in every selected language. Scores and counts must agree.

## Review

Check paired pages side by side for the same claims, commands, limits and status. Check every language switch. Review every visual for stray text from the other language. Structural validation cannot prove translation quality; the agent must perform this review.
