# Häufige Fragen

**Deutsch** | [English](../en/faq.md)

[Start](../../README.md) · [Übersicht](README.md) · [Installation](installation.md) · [Nutzung](usage.md) · [Screens](screens.md) · [FAQ](faq.md)

## Produkt und Zugang

Das Produkt ist ein Plugin mit gebündelten Skills und Claude-Kommandos. Es baut GitHub-Markdown, keinen Shop und keine geschützte Auslieferungsplattform. Es führt weder Commit noch Push noch Veröffentlichung ohne Auftrag aus.

## Voraussetzungen

Der Host benötigt Zugriff auf die Quelle und eine Ausführungsumgebung für die Python-Helfer. Lokale Paketierung benötigt Python 3.10+ und Make; Claude-Installation zusätzlich die Claude-CLI. Ohne geeignete Werkzeuge bleiben automatische Prüfungen offen.

## Datenschutz und Speicherung

Es gibt keinen eigenen Datenbankdienst. Dokumentation und Quellenzeiger liegen im Zielprojekt. Private CVs, Sitzungsdaten, `.env` und Zugangsdaten sind keine Dokumentationsquellen.

## Fehlerbehebung

Bei mehreren gefundenen Skills gib den konkreten Skill-Ordner an. Bei bestehendem Ziel nutze `verify` und gezielte Änderungen. Bei abweichendem vorhandenen Logo entscheidet der Nutzer über dessen Verwendung; das Werkzeug überschreibt es nicht still.

## Grenzen der Prüfung

Die Strukturprüfung führt keinen Zielcode aus und ist kein vollständiger Secret-Scanner. Die Dokumentationsprüfung erkennt fehlende Seiten, Verweise, Überschriften, Sprachwechsel und Platzhalter; fachliche Richtigkeit und Übersetzungsqualität werden zusätzlich inhaltlich geprüft.

---

Dokumentation erstellt mit ZYRIS Skill Documentation. Die Urheberschaft des beschriebenen Produkts bleibt unverändert.
