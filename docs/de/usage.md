# Nutzung

**Deutsch** | [English](../en/usage.md)

[Start](../../README.md) · [Übersicht](README.md) · [Installation](installation.md) · [Nutzung](usage.md) · [Screens](screens.md) · [FAQ](faq.md)

## Einrichten

Die Sprache wird pro Zielrepository festgelegt: nur Deutsch, nur Englisch oder beide. `docs/documentation.json` speichert unter `documentation` beispielsweise `{"languages":["en"],"default_language":"en"}`. Nur Englisch erzeugt `README.md` und `docs/en/`; Deutsch und Sprachwechsel-Links sind dann nicht erforderlich. Fehlt eine klare Auswahl, fragt der Agent zuerst nach. Bestehende Inhalte werden beim Sprachwechsel nicht automatisch gelöscht.

Gib den lokalen Skill- oder Repository-Pfad an. Bei mehreren Skills wird eine Auswahl benötigt. Ohne lokalen Dateizugriff stelle ein bereinigtes Quellarchiv bereit. Ein Pfad auf deinem Rechner wird dadurch nicht automatisch in einer Cloud-Sitzung verfügbar.

## Ablauf auswählen

In Codex wähle das installierte Plugin oder fordere es namentlich an: „Nutze ZYRIS Skill Documentation und prüfe dieses Repository mit verify.“ Die Aktions-Skills für init, update und verify sind im Plugin enthalten; Claude-Slash-Kommandos werden nicht für Codex vorausgesetzt.

In Claude:

```text
/zyris-skill-documentation:verify ../mein-plugin
/zyris-skill-documentation:update ../mein-plugin
/zyris-skill-documentation:init ../mein-skill ../neues-plugin
```

In ChatGPT: „Prüfe mit ZYRIS Skill Documentation die Struktur dieses Plugins.“ oder „Aktualisiere seine Dokumentation auf Deutsch und Englisch.“

## Ausgabe verstehen

Der Strukturbericht unterscheidet Fehler, Warnungen und manuelle Prüfungen. `production_ready: null` bedeutet ausdrücklich: nicht nachgewiesen. `init` erzeugt zunächst Vorlagen; der Agent muss sie anschließend anhand der Quellen ausfüllen.

## Sitzung steuern

Bei Widersprüchen fragt der Agent nach. Du kannst den Umfang begrenzen oder abbrechen. Änderungen erfolgen in einzelnen Dateien; ein Abbruch garantiert kein automatisches Rollback. Prüfe den Git-Diff.

## Später fortsetzen

Starte `update` erneut. `docs/documentation.json` kann den kanonischen Skill und zusätzliche Quellen verorten. Fakten, Versionen und Funktionen werden darin nicht gespeichert; sie werden neu aus den Quellen gelesen.

## Spezialisierte Abläufe

Die Aktion `export` prüft oder baut ein Website-Paket aus vorhandenen Quellen. In Claude: `/zyris-skill-documentation:export REPOSITORY`. In Codex oder ChatGPT fordere den Dokumentationsexport beim Plugin an. Ein Export veröffentlicht nichts und formuliert die Inhalte nicht neu.

`init` akzeptiert nur ein separates, leeres Ziel; `.git`, `.idea` und `.DS_Store` dürfen vorhanden sein. Bestehende Projekte werden zuerst geprüft und nur gezielt verändert. Die vorhandene Quelle wird nicht verschoben. Das neue Projekt erhält eine eigenständige Kopie, keine automatische Synchronisierung.

---

Dokumentation erstellt mit ZYRIS Skill Documentation. Die Urheberschaft des beschriebenen Produkts bleibt unverändert.
