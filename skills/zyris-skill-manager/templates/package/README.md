# ZYRIS Skill Manager

**Deutsch** | [English](README.en.md)

Dieses Plugin dokumentiert zugängliche lokale Skills und Plugins anhand ihrer Quellen. Die Dokumentationssprachen werden pro Repository festgelegt: nur Deutsch, nur Englisch oder beide. Nutze `init` für ein separates leeres Plugin-Grundgerüst, `update` zur Erneuerung der Dokumentation oder `verify` zur lesenden Strukturprüfung. Der Agent fragt bei wesentlichen Unklarheiten nach. Eine erfolgreiche Strukturprüfung bestätigt noch keine Produktionsreife. Das Plugin veröffentlicht und installiert nichts ohne Auftrag.

In Claude: `/zyris-skill-manager:verify QUELLPFAD`, entsprechend `:init` oder `:update`. In ChatGPT fordere die Aktion in natürlicher Sprache an. Die Quelle muss dem Host zugänglich sein; die Helfer benötigen Python 3.10 oder neuer.

[Workflow und Grenzen](skills/zyris-skill-manager/SKILL.md)

## Veröffentlichen mit Freigabe

`/zyris-skill-manager:publish QUELLPFAD` bereitet Diff, Commit-Nachricht und PR vor. Nach Freigabe folgen Commit, Push, PR, Prüfungen und Merge. Keine Version, Tags, Releases oder Katalogpromotion. Der Journalhelfer veröffentlicht selbst nichts. [Workflow](skills/zyris-skill-manager/references/publish.md).
