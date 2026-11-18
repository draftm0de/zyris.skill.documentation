# Repository distribution

The product repository is its own marketplace. Keep root plugin.json, skills/, assets/, .claude-plugin/plugin.json, .claude-plugin/marketplace.json and .agents/plugins/marketplace.json in Git. Generate host metadata with make sync-plugin; check it with make check-plugin. Root metadata is authoritative. Catalog sources point at ./.

No manifest version, tag, GitHub Release, plugin ZIP or separate catalog is required by this workflow. Claude Code falls back to the source commit when neither manifest nor catalog sets a version. Codex Git marketplace upgrades refresh installed copies after repository changes; do not promise that every refresh path watches only commits. Desktop account synchronization varies. Ask users to refresh/sync the marketplace and open a new chat; verify actual content when testing an update.

The user confirmed successful Claude and GPT imports of the Manager repository on 2026-11-18. This is user-reported acceptance of that repository import, not a complete feature/update/uninstall certification and not proof for newly initialized products.

Use actual repository URLs in installation guides. Describe Claude Desktop's reported German path: Einstellungen → Anpassungen / Plugins → + Hinzufügen → Marketplace hinzufügen → Aus einem Repository hinzufügen → URL → Synchronisieren. Codex's reported path: user icon → Settings → Integration > Plugins → + Add > A Marketplace. Label host/account constraints; don't invent an identical UI for ChatGPT web. A private repository needs supported account access.

Sources: https://code.claude.com/docs/en/plugins/loading ; https://support.claude.com/en/articles/13837440-use-plugins-in-claude ; https://developers.openai.com/plugins/build/plugins ; https://learn.chatgpt.com/docs/enterprise/plugin-management . Consult current official docs for changed host claims. Plugin archives are optional developer tests. Website export ZIPs are a separate documentation format.
