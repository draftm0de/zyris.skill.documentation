# Installation

**Deutsch** | [English](../en/installation.md)

<img src="../assets/zyris-icon.png" alt="ZYRIS" width="48">

[Start](../../README.md) · [Übersicht](README.md)

## Plattform auswählen

Claude Desktop und Codex/GPT unterstützen den Repository-Import. Der Nutzer hat beide Importe am 18.11.2026 bestätigt. Zugang, Repository-Berechtigungen und Organisationsrichtlinien gelten weiterhin. Die folgenden Menüpunkte beruhen auf den bereitgestellten Screenshots beziehungsweise Nutzerangaben; ChatGPT-Web-Administration ist ein eigener Weg.

## Installieren

### Claude: grafischer Weg

1. Öffne **Einstellungen**.
2. Scrolle zu **Anpassungen** und wähle **Plugins**.
3. Wähle **+ Hinzufügen → Marketplace hinzufügen**.
4. Wähle **Aus einem Repository hinzufügen**.
5. Gib `https://github.com/draftm0de/zyris.skill.manager` unter **URL** ein und klicke **Synchronisieren**.
6. Wähle den Manager im Marketplace und installiere ihn.

### Claude Code

```text
/plugin marketplace add https://github.com/draftm0de/zyris.skill.manager
/plugin install zyris-skill-manager@zyris-manager
```

### Codex Desktop

Nutzer-Icon → **Settings → Integration > Plugins → + Add > A Marketplace**. Füge dieselbe Repository-URL hinzu und installiere **ZYRIS Skill Manager**.

CLI-Alternative:

```sh
codex plugin marketplace add https://github.com/draftm0de/zyris.skill.manager
codex plugin add zyris-skill-manager@zyris-manager
```

Für den ChatGPT-Workspace-Import verwendet ein Administrator **Admin → Plugins → Add → Import marketplace**. Repository-URL eintragen, Pfad leer lassen; Branch/Tag/Commit kann leer bleiben, um den Standardbranch zu verwenden. Dieser Admin-Weg ist keine Behauptung identischer Menüs in jeder ChatGPT-Oberfläche. Kein Plugin-ZIP erforderlich.

## Aktualisieren

Aktualisiere beziehungsweise synchronisiere den Marketplace und öffne einen neuen Chat. In Claude Code:

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

Entferne das Plugin in der Plugin-Verwaltung oder mit `codex plugin remove zyris-skill-manager@zyris-manager` beziehungsweise `/plugin uninstall zyris-skill-manager@zyris-manager` in Claude Code. Projektdateien und private Journals außerhalb des Caches separat behalten. Entferne alte Documentation-Installationen erst nach erfolgreicher Nutzung des Managers.

## Erste Nutzung prüfen

Öffne einen neuen Chat und bitte mit einem fiktiven Test-Skill um eine Bestandsaufnahme. Prüfe, dass der richtige Quell- und Zielordner verwendet wird. Fehlt das Plugin, kontrolliere Repository-Zugriff, Marketplace und App-Neustart. [Nutzung](usage.md) · [Claude-Hilfe](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) · [OpenAI](https://developers.openai.com/plugins/build/plugins).
