# Installation und Updates

**Deutsch** | [English](../en/installation.md)

[Start](../../README.md) · [Übersicht](README.md) · [Installation](installation.md) · [Nutzung](usage.md) · [Screens](screens.md) · [FAQ](faq.md)

## Plattform auswählen

Claude Code verwendet den lokalen Plugin-Marktplatz. ChatGPT erhält ein Plugin-ZIP; dessen Upload hängt von den Konto- und Workspace-Berechtigungen ab. Das ist keine Installation eines einzelnen Skills.

## Installieren

Für Codex: `make install TARGET=codex` oder `bash install.sh install --target codex`. Der Build erzeugt das native `.codex-plugin/plugin.json` und einen lokalen Codex-Marktplatz. Der Installer registriert diesen mit `codex plugin marketplace add` und installiert das Plugin mit `codex plugin add`. Benötigt eine Codex-CLI mit diesen Befehlen; geprüft mit 0.165.0. Danach einen neuen Codex-Chat öffnen, bei Bedarf Codex neu starten.

```sh
make install TARGET=claude
```

Alternativ: `bash install.sh install --target claude`. Für eine Vorschau: `make install TARGET=claude DRY_RUN=1`. Für ChatGPT: `make package`, dann `dist/zyris-skill-documentation-chatgpt-plugin.zip` in der Pluginverwaltung hochladen. Danach das Plugin im Host aktivieren.

## Aktualisieren

Codex: `make update TARGET=codex` baut neu, registriert denselben lokalen Marktplatz erneut und installiert die neue Inhaltsversion. Der Repository-Ordner muss erreichbar bleiben. Es werden keine einzelnen Skills kopiert oder alte Installationen anderer Marktplätze entfernt.

Alternativ zu Make: `bash install.sh update --target claude`. Beide Aufrufe nutzen dieselbe Implementierung.

Nach Änderungen: `make update TARGET=claude`, anschließend Claude Code neu starten. Zuvor muss der lokale Marktplatz einmal installiert worden sein. `make update TARGET=chatgpt` baut das Paket erneut; die neue Version lädst du manuell hoch. Inhaltsänderungen erzeugen eine neue Paketversion.

## Entfernen

Entferne das Plugin über die Pluginverwaltung des jeweiligen Hosts. Generierte Dokumentation in Ziel-Repositories bleibt dabei erhalten.

## Erste Nutzung prüfen

Starte `verify` mit einem fiktiven Testprojekt. Prüfe, dass der Bericht die Quelle nennt, nichts verändert und offene Abnahmen ausweist. Paketvalidierung ersetzt diesen Host-Test nicht.

---

Dokumentation erstellt mit ZYRIS Skill Documentation. Die Urheberschaft des beschriebenen Produkts bleibt unverändert.
