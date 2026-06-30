# AGENTS.md

## Stack

- Python 3.12+, `uv` for deps
- FastMCP (`mcp[cli]`) — server framework
- `google-cloud-bigquery` — data source
- Pydantic v2 — typed models
- pytest, ruff, mypy

## Dev commands

```bash
uv sync                          # install deps
uv run mcp-google-trends         # start MCP server (stdio transport)
uv run pytest tests/ -v          # all tests
uv run pytest tests/test_tools.py -k test_termos_em_alta  # single test
uv run ruff check src/ tests/    # lint
uv run mypy src/                 # typecheck
npx @modelcontextprotocol/inspector uv run mcp-google-trends  # interactive debug
```

Order: `ruff check -> mypy -> pytest`

## Entrypoint

`src/mcp_google_trends/__main__.py` → calls `server.py`

`server.py` creates `FastMCP` instance, manages BigQuery client via lifespan, imports tools from `tools.py`.

## Tools (3 total, all in `tools.py`)

| Tool | Params | BQ table |
|---|---|---|
| `buscar_termos_em_alta` | pais, data_limite | `international_top_terms` |
| `buscar_termos_emergentes` | pais, data_limite | `international_top_rising_terms` |
| `comparar_termo` | termo, pais, data_inicio, data_fim | `international_top_terms` (aggregated) |

All return Pydantic models (defined in `models.py`), serialized to JSON automatically by FastMCP.

## GCP auth

Uses Application Default Credentials only.
- `gcloud auth application-default login` OR `GOOGLE_APPLICATION_CREDENTIALS=path/to/key.json`
- `GOOGLE_CLOUD_PROJECT` env var must be set
- No hardcoded creds. No pytrends dependency.

## BigQuery quirks

- Use `international_top_terms` and `international_top_rising_terms` (with `country_code`), NOT `top_terms`/`top_rising_terms` (US-only DMA data)
- Tables are partitioned by `week` (DATE type) — always filter with `WHERE week >= @date_threshold` to avoid full scan (costs money)
- Tables only contain the **top ~20 terms per week per country** — most niche/long-tail terms will not appear
- `percent_gain` is INTEGER, not FLOAT
- `score` can be NULL
- Dataset refreshes ~every 24h — intraday data may be stale
- `comparar_termo` does case-insensitive matching (`LOWER(term)`)
- Tools return **empty lists** instead of raising `NoDataError` when no results are found

## Testing

- BigQuery is mocked in `tests/conftest.py` via `unittest.mock.patch`
- Tests use canned result sets matching Pydantic models — no GCP dependency needed
- `conftest.py` provides reusable fixtures for all 3 tools

## Structure boundaries

```
src/mcp_google_trends/     # library code
tests/                     # pytest suite
data/                      # sample outputs for README
```

No other packages or apps. Single-module project.

## Best practices enforced in this repo

- **Typed Python everywhere** — all functions have type annotations; mypy runs in CI-equivalent order
- **Pydantic v2 for data contracts** — tools return validated models, not raw dicts
- **Environment config only** — no hardcoded secrets, regions, or project IDs; everything via env vars validated in `config.py`
- **Custom exceptions** — domain errors (`BigQueryError`, `InvalidCountryError`, `NoDataError`) bubble up instead of bare `Exception`
- **BigQuery client managed via lifespan** — client is created once on startup, closed on shutdown; never created per-request
- **Business logic separated from transport** — `tools.py` has zero FastMCP imports; tools receive a client dependency, not a global
- **Schema-aware SQL** — all queries use parameterized `@` placeholders, not string formatting; date filters are mandatory
- **Tests mock I/O** — no test reaches GCP; fixtures return fake row data matching the real schema
- **Test naming** — `test_<tool_name>_<scenario>` pattern for readability and targeted `-k` filtering
