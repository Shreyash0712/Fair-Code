# Fair Code - contributor task runner.  See CONTRIBUTING.md.
# Reproduces locally what CI runs (.github/workflows: audits.yml, lint.yml,
# build-explainers.yml) so you can catch failures before you push.

.DEFAULT_GOAL := help
PY := python3

.PHONY: help setup test build-explainers favicons lint check

help:  ## Show the available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN{FS = ":.*?## "}{printf "  %-16s %s\n", $$1, $$2}'

setup:  ## Install the package plus the dev tools (pytest, pre-commit)
	$(PY) -m pip install -e ".[excel,parquet,proxy]" pytest pre-commit

test:  ## Run the full test suite (mirrors CI)
	$(PY) -m pytest tests/ -q

build-explainers:  ## Regenerate explainer pages, data.js, sitemap, and OG images (dark + light)
	$(PY) scripts/build_explainers.py
	$(PY) scripts/generate_og_images.py

favicons:  ## Regenerate favicon.ico/PNGs and apple-touch-icon.png from logo.svg
	$(PY) scripts/generate_favicons.py

lint:  ## Enforce the em-dash-free rule (mirrors the lint workflow)
	$(PY) scripts/check_em_dash.py

check: lint test  ## Run everything CI runs (em-dash lint + full test suite)
	@echo "All checks passed."
