# Installation

[Deutsch](../de/installation.md) | **English**

<img src="../assets/zyris-icon.png" alt="ZYRIS" width="48">

[Start](../../README.en.md) · [Guides](README.md)

## Choose your platform

Claude Desktop and Codex/GPT support repository imports. The user confirmed both imports on 2026-11-18. Account access, repository permissions and organizational policies still apply. Menu paths below come from supplied screenshots or user reports; ChatGPT workspace administration is a separate path.

## Install

### Claude Desktop – including the Code tab

The supplied macOS interface is in German; the labels below match that interface.

1. Open **Einstellungen**.
2. Scroll to **Anpassungen** and select **Plugins**.
3. Select **+ Hinzufügen → Marketplace hinzufügen**.
4. Select **Aus einem Repository hinzufügen**.
5. Enter `https://github.com/draftm0de/zyris.skill.manager` under **URL** and select **Synchronisieren**.
6. Select the Manager in the marketplace and install it.

In Claude Desktop 5.11492.5, the user reported that `/plugin install …` and `/plugin marketplace add …` only opened **Settings → Plugins**, without executing the complete request. Use the UI path above in the **Code** tab as well. Opening plugin settings does not confirm installation. The exact internal cause remains unverified; changing JSON indentation does not resolve this behavior.

Anthropic distinguishes the terminal command from the desktop plugin manager: [Desktop documentation](https://code.claude.com/docs/en/desktop#feature-comparison).

### Claude Code in a terminal – optional alternative

The following slash commands apply inside a terminal session started with `claude`. They are not installation instructions for the Desktop Code tab's input field.

1. Add the marketplace:

   ```text
   /plugin marketplace add https://github.com/draftm0de/zyris.skill.manager
   ```

2. Open the plugin details:

   ```text
   /plugin install zyris-skill-manager@zyris-manager
   ```

3. Choose an installation scope and confirm installation.

[Official instructions](https://code.claude.com/docs/en/discover-plugins#install-a-plugin).

### Codex Desktop

1. Open the **user icon** and select **Settings**.
2. Select **Integration → Plugins**.
3. Select **+ Add → A Marketplace**.
4. Enter `https://github.com/draftm0de/zyris.skill.manager as the repository URL and confirm adding it.
5. Select **ZYRIS Skill Manager** and install it.

### Codex in a terminal – optional alternative

Run the following commands directly in the terminal shell.

1. Add the marketplace:

   ```sh
   codex plugin marketplace add https://github.com/draftm0de/zyris.skill.manager
   ```

2. Install the plugin:

   ```sh
   codex plugin add zyris-skill-manager@zyris-manager
   ```

3. Open a new Codex chat and check that the plugin is available.

### ChatGPT – workspace import by an administrator

1. Open **Admin → Plugins**.
2. Select **Add → Import marketplace**.
3. Enter `https://github.com/draftm0de/zyris.skill.manager as the repository URL.
4. Leave **Path** and **Branch/Tag/Commit** empty to use the repository root on the default branch.
5. Start the import and review the result.

This admin path does not imply identical menus in every ChatGPT interface. No plugin ZIP is required.

## Update

In Claude Desktop, refresh or sync through plugin settings, then open a new chat. The following commands are only the alternative for Claude Code in a terminal:

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

Remove the plugin in plugin settings or use `codex plugin remove zyris-skill-manager@zyris-manager` or `/plugin uninstall zyris-skill-manager@zyris-manager` in a Claude Code terminal session. Keep project files and private journals outside the cache. Remove old Documentation installations only after verifying the Manager.

## Verify first use

Open a new chat and request an inventory of a fictional test skill. Confirm the source and output folders. If the plugin is missing, check repository access, the marketplace and app restart. [Usage](usage.md) · [Claude help](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) · [OpenAI](https://developers.openai.com/plugins/build/plugins).
