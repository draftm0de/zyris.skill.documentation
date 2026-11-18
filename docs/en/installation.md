# Installation and updates

[Deutsch](../de/installation.md) | **English**

[Home](../../README.en.md) · [Overview](README.md) · [Install](installation.md) · [Use](usage.md) · [Screens](screens.md) · [FAQ](faq.md)

## Choose your platform

**Preview, checked 2026-11-18. No public ZYRIS catalog or approved release yet.** A final catalog address will be supplied after publication. The source repository is not an installable catalog. A marketplace is a plugin catalog.

| Surface | Requirements and evidence |
|---|---|
| Claude web / Desktop (Chat, Cowork) | Paid Claude account; organization must allow the catalog. German desktop path through the repository dialog evidenced by user screenshots; installation pending. Web in a supported browser; macOS/Windows desktop require separate verification. |
| Claude Code | Configured Claude Code access. Local CLI 2.1.319 on macOS; CLI testing does not prove desktop behavior. |
| Codex Desktop | Plugin-enabled account and permitted catalog. User reported a graphical path to add a catalog; installation remains pending. Organization policies may restrict installation. |
| Codex CLI | Local 0.165.0 on macOS; isolated installation evidence on the development page. Other operating systems not natively tested. |
| ChatGPT | Separate surface and account permissions. Not interchangeable with Codex; package upload acceptance remains open. |

The intended catalog path needs no source checkout, Python or Make. A specific Codex plan is not promised without checking the actual account.

## Install

### Claude graphical interface

**Claude Desktop on macOS, German interface.**

1. Open **Einstellungen** (Settings).
2. Scroll to **Anpassungen** and select **Plugins**.
3. Click **+ Hinzufügen → Marketplace hinzufügen**.
4. Choose **Aus einem Repository hinzufügen**.
5. Under **URL**, enter the published catalog address or use **Repository auswählen**. Supported format: GitHub `owner/repo` or a Git repository URL.
6. Click **Synchronisieren**.

[Official Claude plugin setup help](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) · [Screenshots and verification status](screens.md#native-screenshots).

### Claude Code

After publication, enter `/plugin marketplace add` followed by the approved catalog address in a Claude Code session. Then open `/plugin install zyris-skill-manager@zyris`, review contents and scope, and confirm installation. No invented address is supplied here. [Official instructions](https://code.claude.com/docs/en/discover-plugins).

Claude Code can select a catalog revision with `#TAG`. Official syntax example (not a ZYRIS address):

```text
/plugin marketplace add https://gitlab.example.com/your-group/your-marketplace.git#v1.0.0
```

The tag must exist in the **catalog repository** and contain an installable catalog. It is not automatically the plugin version. A fixed tag does not follow the latest catalog revision. [Official source formats](https://code.claude.com/docs/en/discover-plugins#add-a-marketplace).

### Codex Desktop

1. Open the **User Icon**.
2. Select **Settings**.
3. Open **Integration → Plugins**.
4. Click **+ Add → A Marketplace**.
5. Use the published catalog address in the following dialog.

Menu path reported by the user on 2026-11-18; the next input dialog and installation of our catalog remain to be checked. CLI registration is therefore no longer the default route in this guide.

[Official OpenAI plugin and catalog documentation](https://developers.openai.com/plugins/build/plugins) · [Verification status](release-evidence.md).

### Permissions

Both products bundle instructions and local helpers, without a separate ZYRIS service login. Allow file access only to the intended workspace. Research needs internet access; local helpers need a compatible Python runtime supplied by the host. This is a runtime requirement for those features, not a manual plugin installation step. Without it, persistent storage or document creation must not be reported as successful. Connected services and chat history have their own permissions and retention.

## Update

Claude Code: refresh the catalog and plugin through `/plugin`, then start a new session. Alternatively use `/plugin marketplace update zyris` and `/plugin update zyris-skill-manager@zyris`. Graphical Claude and Codex update controls have not been natively verified here; follow your host's plugin manager and check the displayed version.

Codex CLI: `codex plugin marketplace upgrade zyris`, then `codex plugin add zyris-skill-manager@zyris`. This applies to the future Git catalog, not local test catalog delivery. Back up private data and check it in a new chat after updating. If an update fails, disable the plugin and await a corrected release. Rolling back the catalog does not guarantee that installed caches downgrade.

## Remove

Remove the plugin in the host's plugin manager. CLI alternatives: `codex plugin remove zyris-skill-manager@zyris`, or `/plugin uninstall zyris-skill-manager@zyris` in Claude Code. Organization-required plugins may be locked. Removing a catalog is separate and does not replace uninstalling the plugin. Keep private training data, documents and projects outside plugin caches; delete them separately only if you want to.

## Verify first use

Open a new chat, select the plugin and send **“Document a local skill repository”**. This prompt comes from `plugin.json`; it is not a claimed model response.

Use a fictional test skill in an authorized folder. Request an inspection first and confirm output location and language before generating documentation. See [usage](usage.md).

If the catalog is missing, check its address, publication and admin approval. If the plugin is missing after installation, open a new chat or restart the app. Duplicate entries may come from an older development install; remove that separately only after successful testing. [Developer and release instructions](development.md).

### Migrating from Documentation

The new plugin ID is `zyris-skill-manager`; old installations are named `zyris-skill-documentation`. Once distributed, install and verify Manager before separately removing the old copy. Keep private files and journals. Local renaming has not renamed GitHub or changed active installations.
