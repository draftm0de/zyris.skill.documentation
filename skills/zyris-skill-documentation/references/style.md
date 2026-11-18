# Documentation style

## Voice

Use the repository-selected language(s) and default; read `languages.md`. In both languages, write as a practical colleague: clear, calm and direct. Start with what the product does and who benefits. Use second person for user instructions. Use concrete verbs and short paragraphs; avoid marketing superlatives, hype, filler and invented capabilities.

Use a repeatable reader journey: understand → see an example → install → practise/use → handle storage and errors → maintain. Use tables for parallel choices and numbered lists for sequential actions. Separate user tasks from developer internals.

## Structure

The `templates/outline.json` filenames and level-two headings are the structural contract. Keep their order. Use level-three headings for project-specific detail; do not create empty sections. If a section does not apply, say so briefly with the factual reason. Put a consistent relative navigation row on each page under `docs/`.

Each language’s README remains compact: aim for 100–150 lines, linking deeper details rather than repeating them. Keep one top-level heading per page. Commands go in fenced blocks with the correct language. Provide the working directory and prerequisites; never introduce a command absent from source or verified host documentation.

## Visual system

Use the bundled `zyris-icon.png` at width 48 in the README and documentation index of each language. Reference it with GitHub-compatible relative paths. Use native Markdown for tables and callouts. Optional repo-native SVG transcript previews use navy `#101b2d`, pale panels `#f4f7fc`, teal `#87ddc6`, dark text `#13243a` and a neutral sans-serif font. All previews require an explicit label and provenance in their page language; the design is not a host UI. Produce variants only for selected languages, with identical layout when bilingual. Never mix languages inside a generated graphic.

Use descriptive alt text. Include a visible text explanation for each visual. Do not invent a CI badge or license badge. A CI badge is allowed only when the actual remote and workflow exist. Documentation branding does not change source-product ownership.

## Boundaries

Describe verified local behavior separately from host platform acceptance. A created ZIP is not an installed or published plugin. Chat history is not automatically persistent writable state. Model examples and scores are illustrative, never guarantees. Documentation should be useful without reading the implementation.
