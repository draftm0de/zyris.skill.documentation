# Generated from ZYRIS documentation plugin templates; installation logic is scripts/plugin.py.
export PYTHONDONTWRITEBYTECODE := 1
PYTHON ?= python3
TARGET ?= claude
DRY_RUN ?= 0
.PHONY: package install update check-plugin sync-plugin
package:
	$(PYTHON) scripts/plugin.py build
install:
	$(PYTHON) scripts/plugin.py install --target "$(TARGET)" $(if $(filter 1,$(DRY_RUN)),--dry-run,)
update:
	$(PYTHON) scripts/plugin.py update --target "$(TARGET)" $(if $(filter 1,$(DRY_RUN)),--dry-run,)
check-plugin:
	$(PYTHON) scripts/plugin.py check

sync-plugin:
	$(PYTHON) scripts/plugin.py sync
