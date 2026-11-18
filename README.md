# ZYRIS Skill Manager

**Deutsch** | [English](README.en.md)

<img src="docs/assets/zyris-icon.png" alt="ZYRIS" width="48">

[Dokumentation](docs/de/README.md) · [Screens](docs/de/screens.md)

Ein Plugin für Struktur, Dokumentation, Prüfung und freigabegesteuerte Veröffentlichung von Skills und Plugins.

**Installationsvorschau:** [Claude](docs/de/installation.md#claude-grafischer-weg) · [Claude Code](docs/de/installation.md#claude-code) · [Codex Desktop](docs/de/installation.md#codex-desktop). Öffentliche Katalogadresse und GUI-Abnahme stehen noch aus.

## Für wen ist das gedacht?

Für Entwickler und Teams, die Skills als Plugins anbieten und verständliche GitHub-Dokumentation pflegen möchten. Das Plugin analysiert einen zugänglichen Quellordner und fragt bei relevanten Unklarheiten nach.

## So sieht es aus

Dieses Repository verwendet Deutsch und Englisch mit Deutsch als Standard. Für andere Zielrepositories sind Deutsch, Englisch oder beide frei wählbar. [Ablauf und Screens](docs/de/screens.md) zeigen die Nutzung anhand eines ausdrücklich fiktiven Beispiels. Claude-Desktop-Dialoge sind dokumentiert; vollständige Installations- und Publish-Abnahme bleiben offen.

## Funktionen und Modi

**publish** bereitet Version, Changelog, Commit und PR vor und führt die Veröffentlichung erst nach deiner gebündelten Freigabe aus. [Ablauf und Grenzen](docs/de/publish.md). **export** erzeugt das Website-Dokumentationspaket.


**init** erstellt aus einem Skill ein separates Plugin-Grundgerüst. **update** überarbeitet Dokumentation aus aktuellen Quellen. **verify** prüft Struktur und benennt offene Freigabekriterien. Ordnerprüfungen allein bestätigen keine Produktionsreife.

## Schnellstart

Öffne die [Installationsanleitung](docs/de/installation.md) und wähle Claude oder Codex. Die öffentliche Katalogadresse ist noch nicht freigegeben; die Anleitung ist eine Vorschau. Nach Installation in einem neuen Chat das Plugin auswählen und die dort genannte erste Anfrage senden. Für diesen Nutzerweg ist kein Quellcheckout erforderlich.

## Nutzung

In Claude: `/zyris-skill-manager:verify ../mein-plugin`. Für Dokumentation: `/zyris-skill-manager:update ../mein-plugin`. In ChatGPT wähle das Plugin und beschreibe die gewünschte Aktion; ein lokaler Ordner muss dem Host zugänglich sein.

## Speicherung und Datenschutz

Das Plugin schreibt Markdown, öffentliche Dokumentationsmedien und optional einen Quellenzeiger. Es benötigt keinen eigenen Server. Quelltexte, die du einem KI-Host bereitstellst, unterliegen dessen Verarbeitung. Private Laufzeitdaten und Zugangsdaten gehören nicht in die Dokumentation.

## Projektstatus

MVP mit deterministischen Tests, drei Plugin-Paketformaten und Strukturprüfung. Native Installation, Aktualisierung und inhaltliche Journeys in beiden Hosts bleiben separate Abnahmen. Eine Veröffentlichung oder vollständige Produktionsfreigabe wird nicht behauptet. Lizenz: [MIT](LICENSE).

## Entwicklung

Website-Export aus denselben Quellen: `make check-docs-export` und `make export-docs`. Details stehen in der [Entwicklungsdokumentation](docs/de/development.md).

```sh
make test
make package
make validate-docs OUTPUT=.
make update TARGET=claude
```

`make update` aktualisiert das installierte Dokumentationsplugin. Die Plugin-Aktion `update` aktualisiert dagegen die Dokumentation eines Zielprojekts. [Entwicklung](docs/de/development.md) erklärt Quellen und Paketierung.

---

Dokumentation erstellt mit ZYRIS Skill Manager. Die Urheberschaft des beschriebenen Produkts bleibt unverändert.

Lokale Umbenennung: `zyris.skill.documentation` → `zyris.skill.manager`; Plugin-ID: `zyris-skill-manager`. Das GitHub-Repository bleibt bis zur gesondert freigegebenen Remote-Umbenennung unter seiner bisherigen Adresse. Bestehende Installationen werden nicht automatisch geändert.
