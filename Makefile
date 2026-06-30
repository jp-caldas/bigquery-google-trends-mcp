.PHONY: install sync test lint typecheck check clean build-docker

install:
	uv sync

sync:
	uv sync

test:
	uv run pytest tests/ -v --cov=src/mcp_google_trends --cov-report=term-missing

lint:
	uv run ruff check src/ tests/

typecheck:
	uv run mypy src/

check: lint typecheck test

clean:
	rm -rf .mypy_cache .pytest_cache .ruff_cache
	rm -rf src/mcp_google_trends.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

build-docker:
	docker build -t bigquery-google-trends-mcp .
