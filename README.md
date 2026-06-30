# mcp-google-trends

<p align="center">
  <a href="#english"><kbd>🇺🇸 English</kbd></a>
  <a href="#português"><kbd>🇧🇷 Português</kbd></a>
</p>

<p align="center">
  <i>MCP server que expõe dados do Google Trends via BigQuery</i>
</p>

---

## English

### Features

- **Top terms** — daily most searched terms by country
- **Rising terms** — fastest-growing search terms with percentage gain
- **Term comparison** — track a term's interest score over time

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- A Google Cloud project with **BigQuery API** enabled
- [gcloud CLI](https://cloud.google.com/sdk) installed and authenticated

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/bigquery-google-trends-mcp.git
cd bigquery-google-trends-mcp

# 2. Copy env vars and edit with your GCP project ID
cp .env.example .env
# Edit .env: set GOOGLE_CLOUD_PROJECT=your-gcp-project-id

# 3. Install dependencies
uv sync

# 4. Authenticate with Google Cloud
gcloud auth application-default login

# 5. Verify BigQuery access
uv run mcp-google-trends
```

### Usage

#### Run the MCP server

```bash
uv run mcp-google-trends
```

Starts a stdio-based MCP server listening for tool calls from an LLM client.

#### Connect with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-trends": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/bigquery-google-trends-mcp", "mcp-google-trends"],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "your-gcp-project-id"
      }
    }
  }
}
```

#### Available tools

| Tool | Description | Parameters |
|---|---|---|
| `buscar_termos_em_alta_tool` | Top search terms for a country since a date | `pais` (str), `data_limite` (str `YYYY-MM-DD`) |
| `buscar_termos_emergentes_tool` | Fastest-rising terms with % gain | `pais` (str), `data_limite` (str `YYYY-MM-DD`) |
| `comparar_termo_tool` | Track a term's score over time | `termo`, `pais`, `data_inicio`, `data_fim` |

#### Example prompts for Claude

> "What are the top trending terms in Brazil this week?"
>
> "Show me the fastest rising terms in the US since last month."
>
> "Compare the interest for 'Python' in Brazil between 2024-01 and 2024-06."

#### Interactive debugging

```bash
npx @modelcontextprotocol/inspector uv run mcp-google-trends
```

---

## Português

### Funcionalidades

- **Termos em alta** — termos mais buscados por país
- **Termos emergentes** — termos com maior crescimento percentual
- **Comparação de termos** — acompanhe o score de um termo ao longo do tempo

### Pré-requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Um projeto Google Cloud com **BigQuery API** ativada
- [gcloud CLI](https://cloud.google.com/sdk) instalado e autenticado

### Configuração

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/bigquery-google-trends-mcp.git
cd bigquery-google-trends-mcp

# 2. Copie as variáveis de ambiente e edite com seu GCP project ID
cp .env.example .env
# Edite .env: defina GOOGLE_CLOUD_PROJECT=seu-projeto-gcp

# 3. Instale as dependências
uv sync

# 4. Autentique no Google Cloud
gcloud auth application-default login

# 5. Verifique o acesso ao BigQuery
uv run mcp-google-trends
```

### Uso

#### Iniciar o servidor MCP

```bash
uv run mcp-google-trends
```

Inicia um servidor MCP via stdio, ouvindo chamadas de ferramentas do cliente LLM.

#### Conectar com Claude Desktop

Adicione ao `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-trends": {
      "command": "uv",
      "args": ["run", "--directory", "C:/caminho/para/bigquery-google-trends-mcp", "mcp-google-trends"],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "seu-projeto-gcp"
      }
    }
  }
}
```

#### Ferramentas disponíveis

| Ferramenta | Descrição | Parâmetros |
|---|---|---|
| `buscar_termos_em_alta_tool` | Termos mais buscados em um país desde uma data | `pais` (str), `data_limite` (str `YYYY-MM-DD`) |
| `buscar_termos_emergentes_tool` | Termos com maior crescimento percentual | `pais` (str), `data_limite` (str `YYYY-MM-DD`) |
| `comparar_termo_tool` | Acompanhe o score de um termo ao longo do tempo | `termo`, `pais`, `data_inicio`, `data_fim` |

#### Exemplos de prompts para o Claude

> "Quais são os termos em alta no Brasil esta semana?"
>
> "Mostre os termos emergentes nos EUA desde o mês passado."
>
> "Compare o interesse por 'Python' no Brasil entre janeiro e junho de 2024."

#### Depuração interativa

```bash
npx @modelcontextprotocol/inspector uv run mcp-google-trends
```

---

## Development / Desenvolvimento

```bash
# Run tests / Rodar testes
uv run pytest tests/ -v

# Lint
uv run ruff check src/ tests/

# Type check
uv run mypy src/
```

**Order / Ordem:** `ruff check` → `mypy` → `pytest`

---

## Project structure / Estrutura do projeto

```
src/mcp_google_trends/
├── __main__.py          # Entrypoint
├── server.py            # FastMCP server + lifespan
├── tools.py             # Business logic + SQL queries
├── bigquery_client.py   # BigQuery client wrapper
├── models.py            # Pydantic models (TrendingTerm, RisingTerm, TermComparison)
├── config.py            # Environment config validation
└── exceptions.py        # Custom exceptions
tests/
├── conftest.py          # BigQuery mocks
├── test_tools.py        # Tool unit tests
└── test_server.py       # Server integration tests
data/
├── sample_top_terms.json       # Sample output for top terms
└── sample_rising_terms.json    # Sample output for rising terms
```

---

## Tech stack / Tecnologias

| Library | Purpose / Propósito |
|---|---|
| `mcp[cli]` | MCP server framework (FastMCP) |
| `google-cloud-bigquery` | BigQuery client |
| `pydantic` | Data validation and models |
| `pytest` | Testing |
| `ruff` | Linting |
| `mypy` | Static type checking |

---

## License / Licença

MIT
