# Generated from the documentation plugin template. Content remains Markdown/assets.
PYTHON ?= python3
DOCS_OUTPUT ?=
.PHONY: export-docs check-docs-export
export-docs:
	$(PYTHON) scripts/export_docs.py $(if $(DOCS_OUTPUT),--output "$(DOCS_OUTPUT)",)
check-docs-export:
	$(PYTHON) scripts/export_docs.py --check
