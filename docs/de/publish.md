# Plugin veröffentlichen

## Voraussetzungen

Du brauchst ein zugängliches Plugin-Repository, GitHub-Zugriff über den Host und ein festgelegtes Katalogziel. Ein Quellordner in einer Cloud-Sitzung muss dort tatsächlich verfügbar sein. GitLab-Veröffentlichung ist derzeit nicht integriert.

## Vorschlag anfordern

In Claude: `/zyris-skill-manager:publish PFAD`. In Codex: „Nutze ZYRIS Skill Manager und bereite die Veröffentlichung dieses Plugins vor.“

Der Manager prüft die Änderungen, schlägt eine Version vor und bereitet CHANGELOG.md, Commit-Message und PR-Text vor. Er prüft Pakete und Dokumentation und zeigt, welche Dateien und Ziele betroffen sind. Bis hier entstehen keine Commits, Pushes, PRs oder Releases.

## Gemeinsam freigeben

Du bekommst einen konkreten Vorschlag, etwa:

> Vorgeschlagene Version: 0.2.0. Commit: „feat: add example capability“.
> Soll ich diese Änderungen committen, pushen, den PR erstellen, nach erfolgreichen Prüfungen mergen und anschließend Tag, Release und den genannten Katalog veröffentlichen?

Das ist ein fiktives Beispiel, keine aktuelle Veröffentlichungsanfrage. Du kannst Version, Message und Texte ändern lassen oder ablehnen. Erst deine ausdrückliche Freigabe des gesamten genannten Ablaufs erlaubt die Veröffentlichung. Eine Freigabe nur für einen Commit gilt nicht automatisch für Merge und Release.

## Nach der Freigabe

Der Manager arbeitet die Schritte ab, prüft erforderliche Reviews und Tests und meldet den erreichten Stand. Bestehende Repository-Schutzregeln gelten weiter. Kein manueller Tag und keine Release-Action sind nötig. Normale Test-CI kann weiterlaufen.

## Abbrechen und fortsetzen

Du kannst jederzeit stoppen. Bereits erfolgte öffentliche Schritte werden dadurch nicht automatisch rückgängig. Der Manager speichert ein privates Ablaufjournal außerhalb der Installation und Quellrepositories. Gib beim Fortsetzen dieses Journal und den ursprünglichen Auftrag an; er prüft erst den tatsächlichen Stand. Neue Änderungen brauchen eine neue Freigabe. Keine unbeaufsichtigte Hintergrundveröffentlichung.

## Grenzen

Der Host führt Git- und GitHub-Aktionen aus; der lokale Journalhelfer selbst veröffentlicht nichts. Er belegt weder menschliche Identität noch eine echte Zustimmung. Live-Publikation wurde bei der Implementierung nicht ausgeführt. Ein noch fehlendes Katalogrepository wird nicht automatisch angelegt. Ein Fehler nach Veröffentlichung, aber vor Katalogübernahme, wird als Teilabschluss gemeldet.

[Release-Betrieb](release-operations.md) · [Prüfnachweise](release-evidence.md) · [Nutzung](usage.md)
