# Repository distribution

The product repository is its own marketplace. Keep root plugin.json, skills/, assets/, .claude-plugin/plugin.json, .claude-plugin/marketplace.json and .agents/plugins/marketplace.json in Git. Generate host metadata with make sync-plugin; check it with make check-plugin. Root metadata is authoritative. Catalog sources point at ./.

No manifest version, tag, GitHub Release, plugin ZIP or separate catalog is required by this workflow. Claude Code falls back to the source commit when neither manifest nor catalog sets a version. Codex Git marketplace upgrades refresh installed copies after repository changes; do not promise that every refresh path watches only commits. Desktop account synchronization varies. Ask users to refresh/sync the marketplace and open a new chat; verify actual content when testing an update.

The user confirmed successful Claude and GPT imports of the Manager repository on 2026-11-18. This is user-reported acceptance of that repository import, not a complete feature/update/uninstall certification and not proof for newly initialized products.

Use actual repository URLs in installation guides. Describe Claude Desktop's reported German path: Einstellungen → Anpassungen / Plugins → + Hinzufügen → Marketplace hinzufügen → Aus einem Repository hinzufügen → URL → Synchronisieren. Codex's reported path: user icon → Settings → Integration > Plugins → + Add > A Marketplace. Label host/account constraints; don't invent an identical UI for ChatGPT web. A private repository needs supported account access.

Sources: https://code.claude.com/docs/en/plugins/loading ; https://support.claude.com/en/articles/13837440-use-plugins-in-claude ; https://developers.openai.com/plugins/build/plugins ; https://learn.chatgpt.com/docs/enterprise/plugin-management . Consult current official docs for changed host claims. Plugin archives are optional developer tests. Website export ZIPs are a separate documentation format.

## Claude Desktop versus terminal commands

For Claude Desktop, including its Code tab, document the graphical marketplace flow. Label `/plugin marketplace add` and `/plugin install` examples as Claude Code terminal-session alternatives, never as guaranteed Desktop Code tab installation commands. In the terminal session, `/plugin install` opens details for scope selection and confirmation. A redirect to Settings > Plugins is not proof of registration or installation.

On Desktop 5.11492.5 the user observed that both slash commands opened settings without completing the requested action, while manual UI installation succeeded. This supports a surface-specific limitation; the exact internal command handling was not proven. JSON indentation is not a remedy. Apply the same UI/terminal distinction to update and removal instructions. Source: https://code.claude.com/docs/en/desktop#feature-comparison and https://code.claude.com/docs/en/discover-plugins#install-a-plugin .
