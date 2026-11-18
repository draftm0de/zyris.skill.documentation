# Installation und Updates

**Deutsch** | [English](../en/installation.md)

[Start](../../README.md) · [Übersicht](README.md) · [Installation](installation.md) · [Nutzung](usage.md) · [Screens](screens.md) · [FAQ](faq.md)

## Plattform auswählen

**Vorschau, geprüft am 18.11.2026. Noch kein öffentlicher ZYRIS-Katalog und kein freigegebenes Release.** Die endgültige Katalogadresse fehlt bis zur Veröffentlichung. Verwende nicht die Quellrepository-Adresse als Katalog. Ein Marketplace ist ein Plugin-Katalog.

| Oberfläche | Voraussetzungen und Prüfstatus |
|---|---|
| Claude Web / Desktop (Chat, Cowork) | Bezahlter Claude-Zugang; Organisation muss den Katalog erlauben. Deutscher Desktop-Menüpfad bis zum Repository-Dialog durch Nutzer-Screenshots belegt; Installation offen. Web im unterstützten Browser; Desktop auf macOS/Windows separat prüfen. |
| Claude Code | Eingerichteter Claude-Code-Zugang. Lokale CLI: 2.1.319 auf macOS. CLI-Test ist keine Desktop-Abnahme. |
| Codex Desktop | Konto mit Plugin-Zugang und erlaubtem Katalog. Menüpfad zum Hinzufügen eines Katalogs vom Nutzer mitgeteilt; Installation noch offen. Organisationsrichtlinien können Installation verhindern. |
| Codex CLI | Lokale Version 0.165.0 auf macOS; isolierter Installationstest, siehe Entwicklungsseite. Andere Betriebssysteme nicht nativ geprüft. |
| ChatGPT | Eigenständige Oberfläche und Kontofreigaben. Kein Ersatz für Codex; Upload dieses Pakets bleibt separat abzunehmen. |

Du brauchst für den vorgesehenen Katalogweg keinen Quellcheckout, Python oder Make. Es wird kein bestimmter Tarif für Codex versprochen, solange der konkrete Account nicht geprüft ist.

## Installieren

### Claude: grafischer Weg

**Claude Desktop auf macOS, deutsche Oberfläche.**

1. Öffne **Einstellungen**.
2. Scrolle links zum Abschnitt **Anpassungen** und wähle **Plugins**.
3. Klicke **+ Hinzufügen → Marketplace hinzufügen**.
4. Wähle **Aus einem Repository hinzufügen**.
5. Gib unter **URL** die veröffentlichte Katalogadresse ein beziehungsweise wähle sie über **Repository auswählen**. Unterstütztes Format: GitHub `owner/repo` oder eine Git-Repository-URL.
6. Klicke auf **Synchronisieren**.

[Offizielle Claude-Hilfe zur Einrichtung von Plugins](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) · [Screenshots und Prüfstand](screens.md#echte-screenshots).

### Claude Code

Nach Veröffentlichung in einer Claude-Code-Sitzung zunächst `/plugin marketplace add` gefolgt von der freigegebenen Katalogadresse eingeben. Danach `/plugin install zyris-skill-manager@zyris` öffnen, Umfang und Inhalt prüfen und die Installation bestätigen. Der Platzhalter ist absichtlich kein ausführbarer Installationsbefehl. [Offizielle Anleitung](https://code.claude.com/docs/en/discover-plugins).

Ein bestimmter Katalogstand lässt sich in Claude Code mit `#TAG` auswählen. Offizielles Syntaxbeispiel (keine ZYRIS-Adresse):

```text
/plugin marketplace add https://gitlab.example.com/your-group/your-marketplace.git#v1.0.0
```

Der Tag muss im **Katalogrepository** existieren und dort einen installierbaren Katalog enthalten. Er ist nicht automatisch die Plugin-Version. Ein fest gewählter Tag folgt nicht dem neuesten Katalogstand. [Offizielle Quellenformate](https://code.claude.com/docs/en/discover-plugins#add-a-marketplace).

### Codex Desktop

1. Öffne das **User Icon**.
2. Wähle **Settings**.
3. Öffne **Integration → Plugins**.
4. Klicke **+ Add → A Marketplace**.
5. Verwende die veröffentlichte Katalogadresse im folgenden Dialog.

Menüpfad vom Nutzer am 18.11.2026 mitgeteilt; der folgende Eingabedialog und die Installation unseres Katalogs sind noch zu prüfen. Eine CLI-Einrichtung ist damit nicht mehr der Standardweg dieser Anleitung.

[Offizielle OpenAI-Dokumentation zu Plugins und Katalogen](https://developers.openai.com/plugins/build/plugins) · [Prüfstand](release-evidence.md).

### Berechtigungen

Beide Produkte bündeln Anweisungen und lokale Helfer, keine zusätzliche Anmeldung an einen ZYRIS-Dienst. Erlaube Dateizugriffe nur auf den gewünschten Arbeitsbereich. Recherche benötigt Internetzugang; lokale Helfer benötigen eine passende Python-Laufzeit im Host. Das ist eine Laufzeitvoraussetzung für diese Funktionen, keine manuelle Installationsaufgabe. Fehlt sie, darf dauerhafte Speicherung beziehungsweise Dokumenterzeugung nicht als erfolgreich gelten. Verbundene Dienste und Host-Chatverlauf haben eigene Berechtigungen und Aufbewahrung.

## Aktualisieren

Claude Code: Unter `/plugin` den Katalog aktualisieren, anschließend das Plugin aktualisieren; neue Sitzung starten. Alternativ `/plugin marketplace update zyris` und `/plugin update zyris-skill-manager@zyris`. Grafische Claude- und Codex-Update-Schaltflächen sind hier noch nicht nativ geprüft; folge der Plugin-Verwaltung deines Hosts und kontrolliere die angezeigte Version.

Codex CLI: `codex plugin marketplace upgrade zyris`, danach `codex plugin add zyris-skill-manager@zyris`. Das gilt für den späteren Git-Katalog; lokale Testkataloge werden anders bereitgestellt. Prüfe nach dem Update einen neuen Chat und vorhandene private Daten. Sichere diese Daten vor einem Wechsel. Bei Fehlern Plugin deaktivieren und eine korrigierte Version abwarten. Ein Katalog-Rollback garantiert keinen Downgrade bereits installierter Caches.

## Entfernen

Entferne das Plugin in der Plugin-Verwaltung. CLI-Alternative: `codex plugin remove zyris-skill-manager@zyris` beziehungsweise `/plugin uninstall zyris-skill-manager@zyris` in Claude Code. Organisationsweit vorgeschriebene Plugins können gesperrt sein. Das Entfernen des Katalogs ist ein eigener Schritt und ersetzt die Plugin-Deinstallation nicht. Private Trainingsdaten, Dokumente und Projektdateien außerhalb des Plugin-Caches behalten; lösche sie nur separat auf eigenen Wunsch.

## Erste Nutzung prüfen

Öffne einen neuen Chat, wähle das Plugin und sende: **„Document a local skill repository“**. Diese Beispielanfrage stammt aus `plugin.json`; sie ist keine behauptete Modellantwort.

Verwende einen fiktiven Test-Skill in einem freigegebenen Ordner. Bitte zunächst um eine Bestandsaufnahme; prüfe Zielordner und Sprache vor der Dokumentation. Siehe [Nutzung](usage.md).

Fehlt der Katalog, prüfe Adresse, Veröffentlichung und Admin-Freigabe. Fehlt das Plugin nach Installation, öffne einen neuen Chat beziehungsweise starte die App neu. Doppelte Einträge können von einer früheren Entwicklungsinstallation stammen; diese erst nach erfolgreichem Test separat entfernen. [Entwickler- und Release-Anleitung](development.md).

### Umstieg vom Documentation-Plugin

Die neue Plugin-ID ist `zyris-skill-manager`, die alten Installationen heißen `zyris-skill-documentation`. Installiere nach Bereitstellung den Manager, prüfe seine Fähigkeiten und entferne die alte Kopie erst danach separat. Private Dateien und Journals nicht löschen. Die lokale Umbenennung hat weder das GitHub-Repository noch aktive Installationen geändert.
