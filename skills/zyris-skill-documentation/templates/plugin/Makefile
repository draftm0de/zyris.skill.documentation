include docs.mk
include plugin.mk
.PHONY: help test
help:
	@echo 'make check-docs-export / export-docs  Validate / build the website documentation bundle'
	@echo "make test | package | check-plugin | install/update TARGET=claude|chatgpt|codex"
test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py" -v
