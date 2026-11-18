# ZYRIS Skill Manager

**Deutsch** | [English](README.en.md)

Dieses Plugin dokumentiert zugängliche lokale Skills und Plugins anhand ihrer Quellen. Die Dokumentationssprachen werden pro Repository festgelegt: nur Deutsch, nur Englisch oder beide. Nutze `init` für ein separates leeres Plugin-Grundgerüst, `update` zur Erneuerung der Dokumentation oder `verify` zur lesenden Strukturprüfung. Der Agent fragt bei wesentlichen Unklarheiten nach. Eine erfolgreiche Strukturprüfung bestätigt noch keine Produktionsreife. Das Plugin veröffentlicht und installiert nichts ohne Auftrag.

In Claude: `/zyris-skill-manager:verify QUELLPFAD`, entsprechend `:init` oder `:update`. In ChatGPT fordere die Aktion in natürlicher Sprache an. Die Quelle muss dem Host zugänglich sein; die Helfer benötigen Python 3.10 oder neuer.

[Workflow und Grenzen](skills/zyris-skill-manager/SKILL.md)

## Veröffentlichen mit Freigabe

`/zyris-skill-manager:publish QUELLPFAD` bereitet Version, CHANGELOG.md, Commit-Message, PR-Text, Prüfungen und Ziele vor. Erst nach ausdrücklicher gemeinsamer Freigabe führt der Host Commit, Push, PR, Merge, Tag, Release und Katalogübernahme aus. Keine Release-Action erforderlich. Der gebündelte Journalhelfer unterstützt Wiederaufnahme und prüft geänderte Inhalte; er veröffentlicht selbst nichts. Aktuell ist der konkrete Provider-Ablauf GitHub. [Workflow](skills/zyris-skill-manager/references/publish.md).
