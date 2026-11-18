# Installation

[Deutsch](../de/installation.md) | **English**

<img src="../assets/zyris-icon.png" alt="ZYRIS" width="48">

[Start](../../README.en.md) · [Guides](README.md)

## Choose your platform

Claude Desktop and Codex/GPT support repository imports. The user confirmed both imports on 2026-11-18. Account access, repository permissions and organizational policies still apply. Menu paths below come from supplied screenshots or user reports; ChatGPT workspace administration is a separate path.

## Install

### Claude: graphical path

In the supplied German macOS interface: **Einstellungen → Anpassungen / Plugins → + Hinzufügen → Marketplace hinzufügen → Aus einem Repository hinzufügen**. Enter `https://github.com/draftm0de/zyris.skill.manager` under **URL**, select **Synchronisieren**, then select and install the Manager.

### Claude Code

```text
/plugin marketplace add https://github.com/draftm0de/zyris.skill.manager
/plugin install zyris-skill-manager@zyris-manager
```

### Codex Desktop

User icon → **Settings → Integration > Plugins → + Add > A Marketplace**. Add the same repository URL, then install **ZYRIS Skill Manager**.

CLI alternative:

```sh
codex plugin marketplace add https://github.com/draftm0de/zyris.skill.manager
codex plugin add zyris-skill-manager@zyris-manager
```

For ChatGPT workspace import, an administrator uses **Admin → Plugins → Add → Import marketplace**. Enter the repository URL and leave Path empty. Branch/tag/commit can be empty to follow the default branch. This admin path does not imply identical menus in every ChatGPT interface. No plugin ZIP is required.

## Update

Refresh or sync the marketplace, then open a new chat. In Claude Code:

```text
/plugin marketplace update zyris-manager
/plugin update zyris-skill-manager@zyris-manager
```

In Codex:

```sh
codex plugin marketplace upgrade zyris-manager
```

Committed manifests omit the version. Claude Code then uses the commit as its update identifier. Codex Git marketplace upgrades refresh the installed copy even if its displayed internal cache version stays the same. A push alone does not prove every desktop account has updated. A full update test is separate from the successful initial import.

## Remove

Remove the plugin in plugin settings or use `codex plugin remove zyris-skill-manager@zyris-manager` or `/plugin uninstall zyris-skill-manager@zyris-manager` in Claude Code. Keep project files and private journals outside the cache. Remove old Documentation installations only after verifying the Manager.

## Verify first use

Open a new chat and request an inventory of a fictional test skill. Confirm the source and output folders. If the plugin is missing, check repository access, the marketplace and app restart. [Usage](usage.md) · [Claude help](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) · [OpenAI](https://developers.openai.com/plugins/build/plugins).
