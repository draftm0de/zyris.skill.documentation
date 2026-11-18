# Repository-Veröffentlichung

Das Produktrepository ist zugleich Marketplace. `make sync-plugin` erzeugt Host-Dateien aus `plugin.json`; `make check-plugin` prüft sie. Committe die abgeleiteten Dateien zusammen mit den Quellen. Versionen, Tags, Plugin-ZIPs, GitHub Releases und ein separates Katalogrepository sind nicht erforderlich.

Publish bereitet einen geprüften Diff und eine Commit-Nachricht vor. Nach Freigabe folgen Commit, Push, PR, erforderliche Prüfungen/Reviews und Merge. Eine Korrektur erfolgt über einen neuen geprüften Commit. Kein Force-Push und kein Umgehen von Branch-Schutzregeln.

Die Aktualisierung beim Nutzer ist ein eigener Vorgang: Marketplace synchronisieren und neuen Chat öffnen. Ein erfolgreicher Merge beweist keine automatische Aktualisierung aller Installationen. Optionale Entwicklerarchive und Website-Export-ZIPs bleiben separate Werkzeuge.

[Publish](publish.md) · [Installation](installation.md)
