# Development

[Deutsch](../de/development.md) | **English**

<img src="../assets/zyris-icon.png" alt="ZYRIS" width="48">

[Start](../../README.en.md) · [Guides](README.md)

## Source of truth

`skills/zyris-skill-manager/` contains rules, runtime and canonical templates. Root `plugin.json` owns identity and host metadata. `make sync-plugin` derives the three committed host files; `make check-plugin` detects drift without writing. Capabilities stay under `skills/`, assets under `assets/`.

## Checks

```sh
make check-plugin
make test
make verify SOURCE=.
make validate-docs OUTPUT=.
```

Verify never executes target code. It checks neutral skill paths, versionless import metadata, template copies, ignore rules, static Python imports and documentation pointers. Product behavior tests and host acceptance remain necessary.

## Packaging

Repository import does not require a package build. `make package` remains optional developer tooling for isolated runtime tests. Its hash labels are local cache identifiers, not maintained release versions. Website export: `make check-docs-export` and `make export-docs`.

## CI and releases

The [CI](../../.github/workflows/validate.yml) checks tests, repository metadata and documentation. It publishes nothing. Publish ends at the checked GitHub merge; there are no release Actions, tags or catalog promotion. [Workflow](publish.md) · [Evidence](release-evidence.md).

## Maintain documentation

Update maintains configured languages from current sources. Example: `make init-plugin SOURCE=... OUTPUT=... LANGUAGES="de en" DEFAULT_LANGUAGE=de`. Optional: `REPOSITORY=https://github.com/OWNER/REPO AUTHOR="Confirmed publisher"`. Init creates a separate empty project; the agent then completes its documentation. Website export retains its [contract](../../skills/zyris-skill-manager/references/export-contract.md).
