# Website documentation export contract v1

The exporter is a deterministic build step, not an AI rewrite or a website publisher. Markdown and approved assets remain the only maintained content. Product metadata is read from `plugin.json`; languages are read from `docs/documentation.json.documentation`. The website controls routing, visual layout and rendering.

## Maintained configuration

Add `export` to `docs/documentation.json`:

```json
{
  "schema_version": 1,
  "pages": {
    "overview": {"en": "README.md"},
    "usage": {"en": "docs/en/usage.md"}
  },
  "assets": ["docs/assets/zyris-icon.png"]
}
```

This object contains pointers only, never copied titles, descriptions, versions, license text or capabilities. `overview` is required. Page IDs are stable lowercase identifiers; each page maps exactly the repository's selected languages. Page sources must be the language's root README or Markdown under `docs/<language>/`. Asset paths are explicit, unique, reviewed media under `docs/assets/` or `assets/`; directories and globs are not accepted. Keep the existing language policy authoritative. No extra translations are generated for export.

For a new plugin, `init` supplies page pointers and the shared icon pointer with its documentation scaffold. When `update` adds media or pages, update only these pointers. Unfinished placeholder content cannot be exported. Opting into export in an existing repository also requires the generated `scripts/export_docs.py`, `docs.mk`, and `include docs.mk` in its Makefile. These are snapshots of the canonical templates, not independently maintained implementations. Verify detects drift.

## Commands and output

- `make check-docs-export`: read-only validation; no ZIP or directory is created.
- `make export-docs`: writes `dist/<plugin-name>-documentation.zip`.
- `make export-docs DOCS_OUTPUT=/absolute/export/product.zip`: optional destination outside the repository, or directly under its `dist/`.
- Bundled plugin helper: `documentation.py export --source REPOSITORY [--output FILE.zip] [--check]` uses the trusted plugin exporter without executing code from the target repository.

Do not edit generated ZIPs or `index.json`. Rebuild from source. Publication, commits, pushes and website deployment are separate actions.

The ZIP contains:

```text
index.json
content/README.md
content/README.en.md       # only when selected and not the default language
content/docs/<language>/*.md
content/docs/assets/...   # only explicitly selected assets
```

Paths beneath `content/` preserve repository-relative structure. Markdown and assets are byte-for-byte copies, so GitHub and website consume the same text. The seven legacy `docs/*.md` redirect pages are not selected. Source references, runtime, tests, private state, and repository configuration are not copied into the website bundle.

## Index schema

`index.json` is UTF-8 JSON with these fields:

| Field | Meaning |
|---|---|
| `schema_version` | Integer `1`; reject unsupported versions |
| `format` | Literal `zyris.documentation` |
| `plugin` | Derived `name`, and available `version`, `description`, `license`, `author`, `homepage`, `repository`; optional `display_name` from the manifest interface |
| `documentation` | Existing `languages` and `default_language` policy |
| `source.revision` | Git HEAD commit, or null if unavailable/unborn/not a repository root |
| `source.working_tree_dirty` | Boolean when determined, otherwise null; covers the whole repository and any explicitly exported but untracked/ignored input |
| `source.content_sha256` | SHA-256 of sorted input path/byte records: plugin manifest, documentation configuration and exported content; separated by NUL bytes |
| `pages` | Records with `id`, `language`, H1-derived `title`, `source_path`, `file`, `sha256`, `bytes`, `links` |
| `assets` | Records with `source_path`, `file`, `sha256`, `bytes` |

Pages are ordered by ID then language; assets and ZIP entries by path. ZIP timestamps and permissions are fixed. No build time or machine-specific source path is embedded. Identical inputs and provenance produce identical ZIP bytes. A local modification must never be represented as content of an unchanged commit: dirty/unknown provenance is suitable for previews, not an automatic production publication signal. In a clean checkout, build from a chosen commit/release. The content digest verifies bundle inputs, not authorship or trust.

## Link inventory and website responsibilities

Each `pages[].links[]` record includes its original `href` and a `kind`:

- `page`: `page_id`, `language`, normalized repository `source_path`, `fragment`, `query`. The importer maps this to its own route for that locale/page and retains query and fragment.
- `asset`: `file` inside the archive, plus `source_path`, `fragment`, `query`. Map to the website's asset URL.
- `repository`: `source_path`, `fragment`, `query` for a public source reference, such as a license, runtime reference, test fixture or build script. The file is not bundled. With clean known provenance the website may link to that commit in the canonical repository. Do not invent a pinned URL for dirty/unknown source; handle it explicitly as preview or resolve provenance first.
- `external`: `href` only; HTTP(S) and mailto are accepted. No network requests or external link health checks are performed.

The exporter inventories ordinary inline Markdown links/images, reference link definitions and HTML `href`/`src` attributes outside fenced code and inline code spans. Use uncomplicated relative URLs without spaces or parentheses, or percent-encode them. MDX, executable components and custom Markdown directives are outside v1. The website must parse Markdown itself and apply the inventory; the exporter does not transform prose into HTML or preselect a framework.

Before rendering, the importer must reject ZIP traversal/symlink entries, verify file hashes, support the declared schema version, sanitize rendered Markdown/HTML and handle SVG assets safely. Content is data, not executable build configuration. The export check does not constitute an HTML/SVG security audit or verification of product claims. The importer should fail rather than silently publish unresolved routes or an unselected language. No website importer is implemented by this contract.

## Validation and failure behavior

Missing or duplicate source paths, wrong locale mappings, unsupported versions, duplicated metadata fields in configuration, symlinks, private/cache paths, incomplete placeholders, broken local targets/anchors and undeclared linked docs/media fail validation. Only explicitly declared pages/assets are packaged; local source references are not recursively traversed for inclusion.

All inputs are checked before output publication. A ZIP is built in a temporary file beside the destination and atomically replaced after success; a failed replacement leaves the prior ZIP intact. An unrelated destination ZIP is refused. Inputs are read from a working tree, not locked against concurrent editing: use a stable checkout and serial builds for release reproducibility. Existing content and private workspaces are never modified by the exporter.
