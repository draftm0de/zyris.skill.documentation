include docs.mk
include plugin.mk
export PYTHONDONTWRITEBYTECODE := 1
PYTHON ?= python3
TARGET ?= claude
DRY_RUN ?= 0
SOURCE ?=
OUTPUT ?=
LANGUAGES ?=
DEFAULT_LANGUAGE ?=
TITLE ?=

.PHONY: help test package install update inspect scaffold validate-docs
help:
	@echo 'make check-docs-export / export-docs  Validate / build the website documentation bundle'
	@echo 'make install/update TARGET=codex    Native Codex plugin installation/update'
	@echo 'make verify SOURCE=...             Read-only structure audit; manual release gates remain'
	@echo 'make init-plugin SOURCE=... OUTPUT=...  Scaffold a separate empty plugin repository'
	@echo 'make package                       Build Claude, ChatGPT and Codex plugin ZIPs + local marketplaces'
	@echo 'make install TARGET=claude          Install via native Claude plugin management'
	@echo 'make update TARGET=claude           Rebuild and update the installed Claude plugin'
	@echo 'make update TARGET=chatgpt          Rebuild ZIP; print manual upload instructions'
	@echo 'make install DRY_RUN=1              Build and show native commands without installing'
	@echo 'make inspect SOURCE=/path/to/skill  Inspect source without executing it'
	@echo 'make scaffold SOURCE=... OUTPUT=... Create missing doc templates and copy the icon'
	@echo 'make validate-docs OUTPUT=...       Validate finished docs; scaffolds intentionally fail'
	@echo 'make test                          Deterministic unit/integration tests'

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v
inspect:
	@test -n "$(SOURCE)" || (echo "SOURCE is required" >&2; exit 2)
	$(PYTHON) skills/zyris-skill-manager/scripts/documentation.py inspect --source "$(SOURCE)"
scaffold:
	@test -n "$(SOURCE)" -a -n "$(OUTPUT)" || (echo "SOURCE and OUTPUT are required" >&2; exit 2)
	$(PYTHON) skills/zyris-skill-manager/scripts/documentation.py scaffold --source "$(SOURCE)" --output "$(OUTPUT)" $(if $(TITLE),--title "$(TITLE)",) $(if $(LANGUAGES),--languages $(LANGUAGES),) $(if $(DEFAULT_LANGUAGE),--default-language $(DEFAULT_LANGUAGE),)
validate-docs:
	@test -n "$(OUTPUT)" || (echo "OUTPUT is required" >&2; exit 2)
	$(PYTHON) skills/zyris-skill-manager/scripts/documentation.py validate --output "$(OUTPUT)"

.PHONY: verify init-plugin
verify:
	@test -n "$(SOURCE)" || (echo "SOURCE is required" >&2; exit 2)
	$(PYTHON) skills/zyris-skill-manager/scripts/plugin_audit.py verify --source "$(SOURCE)"
init-plugin:
	@test -n "$(SOURCE)" -a -n "$(OUTPUT)" || (echo "SOURCE and OUTPUT are required" >&2; exit 2)
	$(PYTHON) skills/zyris-skill-manager/scripts/plugin_audit.py init --source "$(SOURCE)" --output "$(OUTPUT)" $(if $(LANGUAGES),--languages $(LANGUAGES),) $(if $(DEFAULT_LANGUAGE),--default-language $(DEFAULT_LANGUAGE),)
