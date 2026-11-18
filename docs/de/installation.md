# Installation

**Deutsch** | [English](../en/installation.md)

<img src="../assets/zyris-icon.png" alt="ZYRIS" width="48">

[Start](../../README.md) · [Übersicht](README.md)

## Plattform auswählen

Claude Desktop und Codex/GPT unterstützen den Repository-Import. Der Nutzer hat beide Importe am 18.11.2026 bestätigt. Zugang, Repository-Berechtigungen und Organisationsrichtlinien gelten weiterhin. Die folgenden Menüpunkte beruhen auf den bereitgestellten Screenshots beziehungsweise Nutzerangaben; ChatGPT-Web-Administration ist ein eigener Weg.

## Installieren

### Claude Desktop – auch im Reiter Code

1. Öffne **Einstellungen**.
2. Scrolle zu **Anpassungen** und wähle **Plugins**.
3. Wähle **+ Hinzufügen → Marketplace hinzufügen**.
4. Wähle **Aus einem Repository hinzufügen**.
5. Gib `https://github.com/draftm0de/zyris.skill.manager` unter **URL** ein und klicke **Synchronisieren**.
6. Wähle den Manager im Marketplace und installiere ihn.

In Claude Desktop 5.11492.5 öffneten beim Nutzer `/plugin install …` und `/plugin marketplace add …` lediglich **Einstellungen → Plugins**; der vollständige Auftrag wurde darüber nicht ausgeführt. Nutze deshalb auch im Reiter **Code** den oben beschriebenen UI-Weg. Das Öffnen der Verwaltung bestätigt keine Installation. Die genaue interne Ursache ist nicht abschließend belegt; Änderungen an der JSON-Einrückung helfen hier nicht.

Anthropic unterscheidet den Terminal-Befehl von der Desktop-Plugin-Verwaltung: [Desktop-Dokumentation](https://code.claude.com/docs/en/desktop#feature-comparison).

### Claude Code im Terminal – optionale Alternative

Die folgenden Slash-Befehle gelten für eine mit `claude` gestartete Sitzung im Terminal. Sie sind keine Installationsanweisung für das Eingabefeld im Desktop-Code-Reiter.

1. Füge den Marketplace hinzu:

   ```text
   /plugin marketplace add https://github.com/draftm0de/zyris.skill.manager
   ```

2. Öffne die Plugin-Details:

   ```text
   /plugin install zyris-skill-manager@zyris-manager
   ```

3. Wähle den Installationsbereich und bestätige die Installation.

[Offizielle Anleitung](https://code.claude.com/docs/en/discover-plugins#install-a-plugin).

### Codex Desktop

1. Öffne das **Nutzer-Icon** und wähle **Settings**.
2. Wähle **Integration → Plugins**.
3. Wähle **+ Add → A Marketplace**.
4. Gib `https://github.com/draftm0de/zyris.skill.manager` als Repository-URL ein und bestätige das Hinzufügen.
5. Wähle **ZYRIS Skill Manager** und installiere ihn.

### Codex im Terminal – optionale Alternative

Die folgenden Befehle werden direkt in der Terminal-Shell ausgeführt.

1. Füge den Marketplace hinzu:

   ```sh
   codex plugin marketplace add https://github.com/draftm0de/zyris.skill.manager
   ```

2. Installiere das Plugin:

   ```sh
   codex plugin add zyris-skill-manager@zyris-manager
   ```

3. Öffne einen neuen Codex-Chat und prüfe, ob das Plugin verfügbar ist.

### ChatGPT – Workspace-Import durch einen Administrator

1. Öffne **Admin → Plugins**.
2. Wähle **Add → Import marketplace**.
3. Gib `https://github.com/draftm0de/zyris.skill.manager` als Repository-URL ein.
4. Lasse **Path** und **Branch/Tag/Commit** leer, um den Repository-Root auf dem Standardbranch zu verwenden.
5. Starte den Import und prüfe das Ergebnis.

Dieser Admin-Weg ist keine Behauptung identischer Menüs in jeder ChatGPT-Oberfläche. Kein Plugin-ZIP erforderlich.

## Aktualisieren

In Claude Desktop verwende die Plugin-Verwaltung zum Aktualisieren beziehungsweise Synchronisieren und öffne danach einen neuen Chat. Die folgenden Befehle sind nur die Alternative für Claude Code im Terminal:

```text
/plugin marketplace update zyris-manager
/plugin update zyris-skill-manager@zyris-manager
```

In Codex:

```sh
codex plugin marketplace upgrade zyris-manager
```

Die eingecheckten Manifeste enthalten keine Version. Claude Code verwendet dann den Commit als Update-Kennung. Codex aktualisiert beim Git-Marketplace-Upgrade die installierte Kopie; seine angezeigte interne Cache-Version kann trotzdem gleich bleiben. Ein Push allein belegt noch keine Aktualisierung in jedem Desktop-Konto. Ein vollständiger Update-Test ist getrennt vom erfolgreichen Erstimport zu prüfen.

## Entfernen

Entferne das Plugin in der Plugin-Verwaltung oder mit `codex plugin remove zyris-skill-manager@zyris-manager` beziehungsweise `/plugin uninstall zyris-skill-manager@zyris-manager` in einer Claude-Code-Terminal-Sitzung. Projektdateien und private Journals außerhalb des Caches separat behalten. Entferne alte Documentation-Installationen erst nach erfolgreicher Nutzung des Managers.

## Erste Nutzung prüfen

Öffne einen neuen Chat und bitte mit einem fiktiven Test-Skill um eine Bestandsaufnahme. Prüfe, dass der richtige Quell- und Zielordner verwendet wird. Fehlt das Plugin, kontrolliere Repository-Zugriff, Marketplace und App-Neustart. [Nutzung](usage.md) · [Claude-Hilfe](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) · [OpenAI](https://developers.openai.com/plugins/build/plugins).
