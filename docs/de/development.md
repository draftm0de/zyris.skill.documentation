# Development

**Deutsch** | [English](../en/development.md)

<img src="../assets/zyris-icon.png" alt="ZYRIS" width="48">

[Start](../../README.md) · [Übersicht](README.md)

## Kanonische Quelle

`skills/zyris-skill-manager/` enthält Regeln, Laufzeit und kanonische Vorlagen. Root-`plugin.json` besitzt Identität und Host-Metadaten. `make sync-plugin` leitet die drei eingecheckten Host-Dateien ab; `make check-plugin` erkennt Drift ohne Schreiben. Fähigkeiten bleiben unter `skills/`, Assets unter `assets/`.

## Prüfungen

```sh
make check-plugin
make test
make verify SOURCE=.
make validate-docs OUTPUT=.
```

Verify führt keinen Zielcode aus. Es prüft neutrale Skill-Pfade, versionslose Importmetadaten, Vorlagenkopien, Ignore-Regeln, statische Python-Imports und Dokumentationsverweise. Eigene Funktionstests und Host-Abnahme bleiben nötig.

## Paketierung

Für den Repository-Import ist kein Paketbau nötig. `make package` bleibt als optionales Entwicklerwerkzeug für isolierte Laufzeittests. Die dortigen Hash-Kennungen sind lokale Cache-Kennungen, keine zu pflegenden Release-Versionen. Website-Export: `make check-docs-export` und `make export-docs`.

## CI und Releases

Die [CI](../../.github/workflows/validate.yml) prüft Tests, Repository-Metadaten und Dokumentation. Sie veröffentlicht nichts. Publish endet beim geprüften GitHub-Merge; es gibt keine Release-Actions, Tags oder Katalogpromotion. [Ablauf](publish.md) · [Nachweise](release-evidence.md).

## Dokumentation pflegen

Update pflegt die gewählten Sprachen aus aktuellen Quellen. Beispiel: `make init-plugin SOURCE=... OUTPUT=... LANGUAGES="de en" DEFAULT_LANGUAGE=de`. Optional: `REPOSITORY=https://github.com/OWNER/REPO AUTHOR="Bestätigter Herausgeber"`. Init erzeugt ein separates leeres Projekt; der Agent vervollständigt anschließend die Dokumentation. Website-Export bleibt bei seinem [Vertrag](../../skills/zyris-skill-manager/references/export-contract.md).
