# ZYRIS Skill Documentation

**Deutsch** | [English](README.en.md)

<img src="docs/assets/zyris-icon.png" alt="ZYRIS" width="48">

[Dokumentation](docs/de/README.md) · [Screens](docs/de/screens.md)

Ein Plugin für konsistente Dokumentation in den pro Repository gewählten Sprachen und nachvollziehbare Strukturprüfungen von Skills und Plugins.

## Für wen ist das gedacht?

Für Entwickler und Teams, die Skills als Plugins anbieten und verständliche GitHub-Dokumentation pflegen möchten. Das Plugin analysiert einen zugänglichen Quellordner und fragt bei relevanten Unklarheiten nach.

## So sieht es aus

Dieses Repository verwendet Deutsch und Englisch mit Deutsch als Standard. Für andere Zielrepositories sind Deutsch, Englisch oder beide frei wählbar. [Ablauf und Screens](docs/de/screens.md) zeigen die Nutzung anhand eines ausdrücklich fiktiven Beispiels. Echte Host-Screenshots stehen noch aus.

## Funktionen und Modi

**init** erstellt aus einem Skill ein separates Plugin-Grundgerüst. **update** überarbeitet Dokumentation aus aktuellen Quellen. **verify** prüft Struktur und benennt offene Freigabekriterien. Ordnerprüfungen allein bestätigen keine Produktionsreife.

## Schnellstart

Voraussetzung: Python 3.10 oder neuer, Make und für native Installation Claude Code.

```sh
make test
make package
make install TARGET=claude
```

Für ChatGPT wird das Plugin-ZIP manuell hochgeladen. Siehe [Installation](docs/de/installation.md).

## Nutzung

In Claude: `/zyris-skill-documentation:verify ../mein-plugin`. Für Dokumentation: `/zyris-skill-documentation:update ../mein-plugin`. In ChatGPT wähle das Plugin und beschreibe die gewünschte Aktion; ein lokaler Ordner muss dem Host zugänglich sein.

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

Dokumentation erstellt mit ZYRIS Skill Documentation. Die Urheberschaft des beschriebenen Produkts bleibt unverändert.
