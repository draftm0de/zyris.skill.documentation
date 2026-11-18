# Storage

**Deutsch** | [English](../en/storage.md)

<img src="../assets/zyris-icon.png" alt="ZYRIS" width="48">

[Start](../../README.md) · [Übersicht](README.md)

## Speichermodell

Dokumentation liegt im Zielrepository; Init erzeugt eine separate Quellkopie. Ein Publish-Journal liegt privat außerhalb von Quelle und Installation.

## Einrichtung und Konfiguration

`docs/documentation.json` speichert Quellenzeiger und Sprache; `plugin.json` enthält Produktmetadaten. Abgeleitete Host-Dateien werden eingecheckt. Temporäre Dateien und `dist/` werden ignoriert.

## Speichern und fortsetzen

Git dokumentiert Änderungen. Der Journalhelfer speichert Plan-Digest, Freigabetext und beobachtete Schritte. Er führt selbst keine externen Aktionen aus.

## Fehler und Wiederherstellung

Nach Unterbrechung zuerst tatsächlichen Git-/PR-Stand prüfen. Keine doppelten Commits oder PRs nach einem Timeout. Geänderte Vorschläge brauchen eine neue Freigabe.

## Einschränkungen

Der Journalinhalt ist kein Identitätsnachweis und ersetzt keine echte Zustimmung. Deinstallation löscht keine externen Projektdateien. Der KI-Host kann bereitgestellte Quellen verarbeiten.
