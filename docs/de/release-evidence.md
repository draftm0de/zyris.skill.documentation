# Release-Prüfnachweis

## Aktueller Stand: Skill Manager

18.11.2026: Manager-Umbenennung und publish-Fähigkeit lokal umgesetzt. Manager: 86 Tests, davon 85 bestanden und ein optionaler Test übersprungen. Interview-Coach: 97 Tests, davon 96 bestanden und ein optionaler Test übersprungen. Die 18 neuen Publish-Tests sind enthalten: konkrete Freigabe, Versions-/Dateikonflikte, unveränderte fremde Arbeit, Journalsperre, Wiederaufnahme und Nutzung aus dem extrahierten Paket. Test-Commits entstehen nur in wegwerfbaren fiktiven Testrepositories; keine Commits in den Produkt-Repositories.

Verify: Manager 35 und Coach 25 Prüfungen ohne Warnungen. Paketbau, Dokumentationsvalidierung und Website-Export erfolgreich. Das umbenannte Manager-Plugin und der Coach wurden in isolierten Claude-Code-/Codex-Profilen installiert, mit geänderten Skill-Inhalten aktualisiert, mit höherer Testversion auf ursprüngliche Inhalte zurückgeführt und entfernt; fiktive private Daten blieben erhalten.

Der Journalhelfer führt keine Git-/GitHub-Veröffentlichung aus. Der veröffentlichende Ablauf ist eine Anweisung an den Host-Agenten mit expliziter Freigabe und überprüften Zwischenständen. Ein echter entfernter Commit/Push/PR/Merge/Release/Kataloglauf wurde nicht ausgeführt. Keine Produktionsabnahme für die Remote-Orchestrierung behauptet. Die öffentliche GitHub-Adresse bleibt unverändert. Alte generierte Documentation-Artefakte wurden zur Erhaltung unter `.tmp/pre-manager-dist/` archiviert; aktive Installationen wurden nicht geändert.

## Historischer Stand vor der Manager-Umstellung

2026-11-18 · macOS · Claude Code 2.1.319 · Codex CLI 0.165.0.

Lokale Testdistribution, kein öffentliches Release. Die sichtbaren Desktop-Anwendungen gehören zum persönlichen Profil; kein isoliertes GUI-Testkonto festgestellt und keine Installation dort verändert.

| Prüfung | Ergebnis |
|---|---|
| Coach unit + regression | 95 tests, 1 optional native test skipped |
| Documentation | 66 tests, 1 optional native test skipped |
| Release contract | 12 tests per repository, included above: versions/tags, clean commit, deterministic retry, corruption, locks, failed atomic write, partial upload, catalog completeness |
| Native CLI / both products | Install A (0.1.0), runtime update to fictional B (0.1.1), forward recovery C (0.1.2), uninstall: passed in both hosts |
| Private fixture | Separate fictional progress file preserved byte-for-byte |
| Extracted runtime | Existing package lifecycle/initialization regression tests passed |
| GUI / screenshots / model conversation | User screenshots establish German Claude Desktop navigation through repository selection; sync/install and model conversation remain unverified |
| Public catalog / public release | Not published; final acceptance pending |

Der native Lauf verwendete temporäre HOME-, CODEX_HOME- und CLAUDE_CONFIG_DIR-Verzeichnisse, den generierten gemeinsamen Katalog und ein Arbeitsverzeichnis außerhalb beider Quellcheckouts. Testversion 0.1.1 änderte die Skill-Dateien; 0.1.2 stellte deren ursprüngliche Bytes wieder her. Die installierten bzw. vom Host geladenen Skill-Ressourcen wurden byteweise mit dem Katalog verglichen. Es fand kein Modellaufruf statt. Private Daten wurden nicht gelesen. Nachweise lokaler Läufe liegen im ignorierten Arbeitsordner des Auftrags; keine privaten Rohlogs werden exportiert.

Ein realer öffentlicher Git-Katalog, Kontorechte, grafische Updates und Downgrades bleiben offen. Die lokale Wiederherstellung durch atomare Wiederholung ist getestet; ein nativer Downgrade wurde nicht nachgewiesen. Sichere Betriebsstrategie: höhere Patchversion mit bekannt gutem Runtime-Stand. Offene Aufnahmen: [Beispiele](screens.md). Ablauf und Freigaben: [Release-Betrieb](release-operations.md).

Weitere Prüfungen: Dokumentationsvalidierung, Paketbau und Website-Export erfolgreich; Verify 34 Prüfungen ohne Warnungen. Lokale grafische App-Versionen nur aus App-Metadaten gelesen: ChatGPT/Codex 26.1111.21308 (27194), Claude Desktop 5.11492.5. Das ist keine UI-Abnahme.

Nativen Lauf wiederholen (isolierte Profile, beide CLIs erforderlich):

```sh
python3 -B scripts/test_release_native.py --bundle dist/release-preview-final --output .tmp/native-release.json
```

Nachtrag: Nutzeraufnahmen vom 18.11.2026 belegen den deutschen Claude-Desktop-Menüpfad bis zur Repository-Eingabe. Zwei Dialogbilder sind auf der [Beispielseite](screens.md) enthalten. Keine erfolgreiche Synchronisierung oder Produktinstallation aus diesen Bildern abgeleitet.

Codex-UI-Nachtrag: Der Nutzer meldet **User Icon → Settings → Integration → Plugins → + Add → A Marketplace**. Damit ist ein grafischer Einstieg berichtet; Folgedialog, Katalogimport und Plugin-Installation sind nicht durch Screenshots oder einen eigenen Lauf bestätigt.
