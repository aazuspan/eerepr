.PHONY: install-hooks clean-build docs view-docs
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

# Print the comment for each make command
for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean-build: ## Remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

install: ## Install the package
	pip install .

install-dev: ## Install development version and pre-commit hooks
	pip install -e .[dev]

release: ## Package and upload
	python setup.py sdist
	twine upload dist/*

tests: ## Run unit tests
	pytest .

coverage: ## Run unit tests and produce a coverage HTML
	pytest . --cov=eerepr --cov-report=html

view-coverage: ## Open coverage HTML in a browser
	python -m webbrowser -t htmlcov/index.html