# ZYRIS Skill Manager

**Deutsch** | [English](README.en.md)

<img src="docs/assets/zyris-icon.png" alt="ZYRIS" width="48">

## Für wen ist das gedacht?

Für Entwickler und Teams, die Skills als installierbare Plugins pflegen. Der Manager unterstützt Struktur, Dokumentation, Prüfung, Website-Export und die Veröffentlichung über einen geprüften GitHub-PR.

## So sieht es aus

Ein Plugin mit sechs Skill-Einstiegspunkten. [Beispiel und echte Claude-Dialoge](docs/de/screens.md) zeigen den Ablauf. Der Nutzer hat den Repository-Import in Claude und GPT am 18.11.2026 bestätigt.

## Funktionen und Modi

**init** erzeugt ein separates Plugin-Grundgerüst. **update** pflegt Dokumentation anhand der Quellen. **verify** prüft Struktur und Metadaten. **export** erzeugt das Website-Dokumentationspaket. **publish** schlägt die Commit-Nachricht vor und führt nach Freigabe Commit, Push, PR und Merge aus. [Publish im Detail](docs/de/publish.md).

## Schnellstart

Füge `https://github.com/draftm0de/zyris.skill.manager` in der Plugin-Verwaltung als Marketplace hinzu und installiere **ZYRIS Skill Manager**. Kein ZIP und kein Tag nötig. [Installationswege](docs/de/installation.md).

## Nutzung

Wähle das Plugin und sage: „Prüfe dieses Repository mit verify.“ Für Dokumentation: „Aktualisiere die Dokumentation auf Deutsch und Englisch.“ In Claude Code sind auch `/zyris-skill-manager:verify PFAD` und die weiteren Aktionskommandos verfügbar. [Nutzung](docs/de/usage.md).

## Speicherung und Datenschutz

Der Manager schreibt Dokumentationsdateien und bei init eine separate Quellkopie. Publish-Journals liegen außerhalb von Quelle und Plugin-Installation. Private Daten, Zugangsdaten und fremde Änderungen werden nicht übernommen. Der KI-Host verarbeitet die bereitgestellten Quellen nach seinen Bedingungen.

## Projektstatus

Repository-Import in Claude und GPT vom Nutzer bestätigt. CLI-Import wurde zusätzlich isoliert getestet. Das bestätigt weder sämtliche Funktionen noch automatische Updates oder den vollständigen Publish-Ablauf. Lizenz: [MIT](LICENSE). [Prüfstand](docs/de/release-evidence.md).

## Entwicklung

```sh
make sync-plugin
make check-plugin
make test
make verify SOURCE=.
make validate-docs OUTPUT=.
make check-docs-export
```

`make sync-plugin` erzeugt die einzucheckenden Host-Metadaten. `make update TARGET=codex` aktualisiert die installierte Remote-Kopie; die Skill-Aktion **update** pflegt dagegen Dokumentation. [Entwicklung](docs/de/development.md).
