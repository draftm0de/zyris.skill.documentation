# Release-Betrieb

## Verantwortlichkeit

ZYRIS Skill Manager führt Veröffentlichungen in der aktiven Sitzung aus. Es gibt keine Release-Action und keinen Hintergrunddienst. Die normale Test-CI bleibt bestehen. Eine Implementierungs-, Prüf- oder Vorbereitungsanfrage veröffentlicht nichts.

## Version und Changelog

`plugin.json` ist die einzige gepflegte aktuelle Produktversion. `CHANGELOG.md` enthält die Historie mit `## [X.Y.Z]`, Änderungen, Grenzen und Upgrade-Hinweisen. Release Notes werden beim Build aus diesem Abschnitt abgeleitet. Keine parallele Pflege unter docs/releases. Der publish-Ablauf verwendet stabile SemVer-Versionen; Entwicklungsbuilds behalten den Inhaltshash. Der Paketbauer unterstützt separat Vorabversionen.

## Ablauf

1. Änderungen und entfernte Versionsstände prüfen, explizite Dateiauswahl treffen und fremde Arbeit erhalten.
2. Version, Changelog, Commit-Message, PR-Titel/-Beschreibung und Veröffentlichungsziele vorbereiten. Tests, Verify, Dokumentationsvalidierung, Paketbau und Export prüfen.
3. Den konkreten Vorschlag einschließlich Katalogziel zeigen. Eine Freigabe für Commit, Push, PR, Merge, Tag, Release und Katalogübernahme einholen. Änderungswünsche zuerst einarbeiten; Schweigen ist keine Zustimmung.
4. Nach Freigabe den passenden Feature-Branch committen, pushen und einen PR erstellen. Erfolgreiche Prüfungen und erforderliche Reviews abwarten. Keine Schutzregeln umgehen.
5. Den tatsächlichen Merge-Commit prüfen und taggen. Daraus ein reguläres Bundle erzeugen, veröffentlichen und den vollständigen Katalog über den freigegebenen Weg übernehmen.

Einmal genehmigte Schritte benötigen keine erneute Einzelbestätigung. Geänderte Inhalte, Versionen, Texte oder Ziele brauchen einen neuen Vorschlag. Nur ein Commit oder PR darf nicht als Freigabe für die gesamte Veröffentlichung interpretiert werden.

## Werkzeuge

Die Ausführung übernimmt die publish-Fähigkeit des Managers über Git und GitHub-Werkzeuge. Der gebündelte Helfer `publish_plan.py` erstellt und prüft den lokalen Freigabeplan und protokolliert beobachtete Schritte; er führt selbst keine Veröffentlichung aus. Das Journal gehört in einen privaten Ordner außerhalb von Quellrepository und Plugin-Installation. Es enthält Dateihashes, Version, Texte, Freigabeantwort und Commit-/PR-/Release-Nachweise, keine Zugangsdaten. Ein Journal ersetzt keine tatsächliche Zustimmung im Gespräch.

Die generischen Werkzeuge `scripts/release.py`, `scripts/publish.py` und `scripts/test_release_native.py` bleiben kanonische Build-/Release-Helfer. Der niedrigstufige Publisher darf erst im genehmigten Ablauf aufgerufen werden. Beispiele für reine lokale Vorbereitung:

```sh
make test check-plugin check-docs-export export-docs
python3 -B scripts/release.py prepare --tag v0.1.0 --preview --output dist/manager-preview
```

Das reguläre Bundle verlangt einen sauberen Checkout und einen Tag auf HEAD. Vorschauen sind gekennzeichnet und nicht regulär publizierbar. ZIPs, SHA256SUMS und release.json werden deterministisch erzeugt; identische Wiederholungen sind erlaubt, abweichende Ausgaben werden nicht überschrieben. Unterschiedliche Kompressionsbibliotheken können abweichende Bytes erzeugen; Wiederholungen verwenden dieselbe Toolchain.

## Katalog und Repository-Adressen

Quellrepository, Release-Bundle, installierbarer Katalog und öffentliche Host-Listung sind getrennte Dinge. Die bestehenden Produktadressen enthalten bisher keine installierbaren Katalogdateien. Ein gemeinsamer generierter Katalog bleibt ein Vorschlag; alternativ sind generierte Distributionszweige möglich. Kein neues Repository wird durch publish automatisch angelegt. Vor Freigabe müssen das vorhandene Katalogziel, Branch, erwarteter Commit und vollständige Produktmenge feststehen. Host-Unterstützung des gewählten Weges bleibt zu prüfen.

Ein Produkt bleibt ein Plugin. Generierte Host-Manifeste und Runtime-Kopien im Katalog sind keine separat gepflegten Quellen. `provenance.json` ordnet Produkte ihren Release-Commits und Prüfsummen zu. Beim Katalog-PR wird die gesamte gewünschte Produktmenge geprüft, damit andere Plugins erhalten bleiben.

## Wiederaufnahme und Fehler

Nach Unterbrechung Journal und tatsächliche Git-/GitHub-Zustände abgleichen. Keine zweite Commit-/PR-/Release-Erstellung nach einem unklaren Timeout. Bestehende identische Tags/Artefakte wiederverwenden; abweichende niemals überschreiben. Fehlgeschlagene Checks blockieren den Merge. Ein erforderliches fremdes Review kann das Plugin nicht ersetzen. Ein veröffentlichtes Release mit noch fehlender Katalogpromotion ist nur teilweise abgeschlossen.

Lokale Journalsperren schützen nicht vor anderen Remote-Schreibern. Vor jeder Änderung erwartete Commit-Stände prüfen; kein force-push, keine verschobenen Tags und kein Admin-Bypass. Geänderte Katalogstände neu vorbereiten und freigeben lassen. Ein verwaister Lock darf erst nach Prüfung des beendeten Schreibers entfernt werden.

Bei fehlerhaften Releases eine höhere Patchversion mit bekannt gutem Runtime-Stand vorbereiten. Ein Katalog-Revert garantiert keinen Downgrade vorhandener Caches. Private Daten bleiben separat erhalten. Rückkehr und Update werden isoliert geprüft.

## Grenzen und Prüfstand

Der konkrete Ablauf unterstützt derzeit GitHub. GitLab-MR-/Release-Automation ist nicht implementiert. GitHub-Anmeldung, ausreichende Rechte und ein vorhandenes Katalogziel sind erforderlich; das Plugin erweitert keine Rechte. Es läuft nur während einer aktiven Sitzung und kann nach Abbruch anhand des Journals fortgesetzt werden.

[Prüfnachweise](release-evidence.md). Live-Veröffentlichung, öffentliche Installation, Kontorechte und vollständige GUI-Abnahme sind nicht durch lokale Tests bewiesen. Keine Commits, Tags, Pushes, Remote-Umbenennungen oder Veröffentlichungen wurden bei dieser Umsetzung ausgeführt. `www.draftmode` bleibt unverändert.
