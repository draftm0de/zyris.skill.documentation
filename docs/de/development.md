# Entwicklung

**Deutsch** | [English](../en/development.md)

[Start](../../README.md) · [Übersicht](README.md) · [Installation](installation.md) · [Nutzung](usage.md) · [Screens](screens.md) · [FAQ](faq.md)

## Kanonische Quelle

Der [Hauptworkflow](../../skills/zyris-skill-manager/SKILL.md) und seine Referenzen definieren das Verhalten. Die dünnen Aktions-Skills verweisen darauf. `plugin.json` enthält die Basisversion; der Build leitet die Host-Manifeste ab. Dokumentation und kopiertes Logo sind abgeleitete Ausgaben.

Die gemeinsame Quellstruktur verwendet für alle Hosts `skills/<name>/` im Plugin-Projektroot. `init` erzeugt sie; `verify` beanstandet abweichende konfigurierte Wurzeln, Host-lokale Skill-Quellen und Host-Manifeste im Quellroot. Alte Strukturen bleiben für Analyse und ausdrückliche Migration erkennbar, sind aber kein alternativer Standard. Ein Plugin kann mehrere Fähigkeiten ohne getrennte Installationen enthalten.

Gemeinsame Ablageregeln: `.tmp/` entsteht erst für lokale Arbeitsdateien oder Diagnoseausgaben; `dist/` enthält erzeugte Pakete. `.DS_Store`, `.idea/`, Caches, Bytecode und Abhängigkeitsumgebungen werden ignoriert. Projektspezifische Ignore-Regeln und Diagnosen bleiben erhalten. Entwicklungswerkzeuge liegen in Root-`scripts/`, Laufzeit-Scripts beim jeweiligen Skill. Lokale Python-Imports sollen keinen Bytecode erzeugen; entpackte Pakete werden unabhängig vom Checkout getestet. Verify des Dokumentationsplugins prüft wirksame Ignore-Regeln, versionierte Ausgabedateien und statisch Python-Syntax/Imports im Paket; es führt keinen Zielcode aus und ersetzt keine Host-Abnahme.

## Prüfungen

`ZYRIS_TEST_CODEX_NATIVE=1 make test` aktiviert zusätzlich einen echten Codex-CLI-Test in einem isolierten temporären Profil: Installation, erneute Installation und Update nach einer Inhaltsänderung. Das persönliche Codex-Profil bleibt dabei unberührt.

```sh
make test
make validate-docs OUTPUT=.
make verify SOURCE=.
```

`verify` liefert bei Fehlern oder Warnungen Exit-Code 1. Eine fehlende Lizenzentscheidung oder noch offene Dokumentation wird sichtbar; das ist kein Grund, Prüfungen abzuschwächen. Echte Host-Journeys bleiben zusätzlich erforderlich.

## Paketierung

Die kanonische Installationsimplementierung liegt in `skills/zyris-skill-manager/templates/plugin/`. `scripts/plugin.py`, `install.sh` und `plugin.mk` im jeweiligen Projekt sind daraus erzeugte Kopien; `verify` erkennt Abweichungen. Name, Basisversion und Metadaten kommen aus `plugin.json`. Die Erweiterung `io.zyris.distribution` legt `skillRoot`, optional `marketplace` und optionale zusätzliche Paketdateien (`files`: Ziel → Quelle) fest. Alle Host-Manifeste werden beim Build abgeleitet.

`make package` baut reproduzierbare Claude-, ChatGPT- und Codex-Plugin-ZIPs sowie lokale Claude- und Codex-Marktplätze in `dist/`. Quellen mit Symlinks werden zurückgewiesen. Laufzeit, Vorlagen und Icon bestimmen den Versionshash; Entwicklerdateien werden nicht verteilt.

## CI und Releases

[Release-Betrieb und Freigaben](release-operations.md) · [Prüfnachweis](release-evidence.md).


Die [CI](../../.github/workflows/validate.yml) führt Tests, Paketbau und Dokumentationsvalidierung aus. Sie veröffentlicht nichts. Ein erfolgreicher lokaler Lauf beweist weder einen erfolgreichen Remote-Lauf noch eine Host-Abnahme.

## Dokumentation pflegen

### Export für die Website

`make check-docs-export` prüft den Vertrag; `make export-docs` erzeugt `dist/<plugin-name>-documentation.zip` mit `index.json`, unveränderten Markdown-Seiten und ausgewählten Assets. Die Konfiguration `export` in `docs/documentation.json` enthält ausschließlich Seiten- und Asset-Verweise. Produktmetadaten kommen aus `plugin.json`, Sprachen aus der bestehenden Dokumentationskonfiguration. Der Index ergänzt Linkzuordnungen, Prüfsummen und Git-Herkunft; lokale Änderungen werden kenntlich gemacht. Die Website übernimmt Routing und sichere Darstellung. Es wird nichts veröffentlicht.

[Exportvertrag v1](../../skills/zyris-skill-manager/references/export-contract.md)

Starte die Plugin-Aktion `update` und prüfe den Git-Diff beider Sprachen. Nutze `make scaffold SOURCE=... OUTPUT=...` nur für fehlende Vorlagen; der Helfer formuliert keine Inhalte. `make init-plugin SOURCE=... OUTPUT=...` erzeugt ein separates Grundgerüst mit Manifesten, Build, Starttests, CI und Dokumentationsvorlagen.

---

Dokumentation erstellt mit ZYRIS Skill Manager. Die Urheberschaft des beschriebenen Produkts bleibt unverändert.

Für neue Projekte: `make init-plugin SOURCE=... OUTPUT=... LANGUAGES=en DEFAULT_LANGUAGE=en`. `make scaffold` unterstützt dieselben Sprachparameter; bestehende Projektkonfigurationen werden bei Widersprüchen geschützt.
