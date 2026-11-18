# Usage

**Deutsch** | [English](../en/usage.md)

<img src="../assets/zyris-icon.png" alt="ZYRIS" width="48">

[Start](../../README.md) · [Übersicht](README.md)

## Einrichten

Gib einen zugänglichen Quellordner an. Sprache und Zielordner werden pro Repository geklärt; `docs/documentation.json` speichert nur Quellenzeiger, Sprache und Exportkonfiguration. Ohne lokalen Dateizugriff muss eine bereinigte Quellkopie bereitgestellt werden.

## Ablauf auswählen

Wähle init, update, verify, export oder publish. In Claude Code beispielsweise `/zyris-skill-manager:init QUELLE ZIEL`. In Codex/GPT wählst du die passende Fähigkeit oder beschreibst die Aktion. Die Claude-Slash-Oberfläche wird nicht für jeden Host vorausgesetzt.

## Ausgabe verstehen

Init erzeugt eine separate Kopie unter `skills/`, ein versionsloses Manifest, beide Marketplace-Dateien, das Claude-Manifest und Entwicklungs-/Dokumentationsvorlagen. Fehlende Repository-URL und Herausgeberangaben müssen geklärt werden. Vorlagen allein sind noch keine fertige Produktdokumentation. Verify unterscheidet Fehler, Warnungen und manuell offene Prüfungen; `production_ready: null` ist keine Freigabe.

## Sitzung steuern

Beschränke den Auftrag auf gewünschte Dateien oder Aktionen. Init überschreibt keine bestehenden Projekte. Bei vorhandenen Projekten werden Änderungen gezielt vorgenommen; prüfe anschließend den Diff. Ein Abbruch macht bereits erfolgte Änderungen nicht automatisch rückgängig.

## Später fortsetzen

Update liest aktuelle Quellen erneut. Publish kann mit einem privaten Journal fortgesetzt werden, nachdem tatsächlicher GitHub-Stand und ursprüngliche Freigabe überprüft wurden. Alte Release-Journals benötigen einen neuen Plan.

## Spezialisierte Abläufe

[Publish](publish.md) schlägt die Commit-Nachricht vor und führt nur nach Freigabe Commit → Push → PR → Prüfungen → Merge aus. Keine Versionsfreigabe, Tags oder Releases. Export baut dagegen ein ZIP für die Website aus vorhandenem Markdown; dieses ZIP ist kein Installationspaket.
