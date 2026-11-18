# Speicherung und Wiederherstellung

**Deutsch** | [English](../en/storage.md)

[Start](../../README.md) · [Übersicht](README.md) · [Installation](installation.md) · [Nutzung](usage.md) · [Screens](screens.md) · [FAQ](faq.md)

## Speichermodell

Dateien im Zielrepository sind das Ergebnis. `README.md` und `docs/de/` sind Deutsch, `README.en.md` und `docs/en/` Englisch. Das gemeinsame Logo liegt unter `docs/assets/zyris-icon.png`.

## Einrichtung und Konfiguration

Der optionale Quellenzeiger enthält `schema_version`, optional `source_skill`, `extra_sources`, `open_questions` und die Sprachkonfiguration `documentation`. Relative Quellen müssen im Repository liegen. Bei externen Quellen werden nur die Dokumentationseinstellungen gespeichert; gib die Quelle beim nächsten Aufruf erneut an.

## Speichern und fortsetzen

Änderungen werden als normale Dateien gespeichert. Bei Wiederaufnahme liest der Agent die kanonischen Quellen erneut. Erledigte Fragen werden entfernt oder in der maßgeblichen Quelldatei geklärt; Produktbeschreibungen werden nicht im Manifest dupliziert.

## Fehler und Wiederherstellung

Scaffolding überschreibt keine vorhandenen Seiten. `init` verweigert gefüllte Ziele. Bei Schreibfehlern können bereits erstellte Dateien zurückbleiben; prüfe den Diff und setze gezielt fort. Eine projektweite Transaktion oder gleichzeitige Bearbeitung mehrerer Agenten wird nicht garantiert.

## Einschränkungen

Keine automatische Cloud-Synchronisierung, keine dauerhafte Chat-Erinnerung und kein Backupdienst. Nutze die Versionsverwaltung des Zielprojekts. Ein Commit bleibt eine separate, ausdrücklich beauftragte Aktion.

---

Dokumentation erstellt mit ZYRIS Skill Manager. Die Urheberschaft des beschriebenen Produkts bleibt unverändert.

### Publish journal

Das private Freigabejournal liegt außerhalb der Plugin-Installation und des Quellrepositories. Es enthält ausgewählte Dateipfade/Hashes, Nachrichtenentwürfe, die konkrete Freigabeantwort und Veröffentlichungsnachweise. Keine Tokens speichern; Journal für Wiederaufnahme behalten und erst auf eigenen Wunsch löschen. Siehe [publish](publish.md).
