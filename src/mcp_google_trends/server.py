from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from google.cloud import bigquery
from mcp.server.fastmcp import FastMCP

from . import config
from .bigquery_client import create_client
from .tools import buscar_termos_em_alta, buscar_termos_emergentes, comparar_termo

_bq_client: bigquery.Client | None = None


def _get_client() -> bigquery.Client:
    if _bq_client is None:
        raise RuntimeError("BigQuery client not initialized. Call lifespan first.")
    return _bq_client


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[dict[str, Any]]:
    global _bq_client
    config.validate()
    _bq_client = create_client()
    try:
        yield {}
    finally:
        _bq_client.close()  # type: ignore[no-untyped-call]
        _bq_client = None


mcp = FastMCP("Google Trends", lifespan=lifespan)


@mcp.tool()
def buscar_termos_em_alta_tool(pais: str, data_limite: str) -> list[dict[str, Any]]:
    return [m.model_dump() for m in buscar_termos_em_alta(_get_client(), pais, data_limite)]


@mcp.tool()
def buscar_termos_emergentes_tool(pais: str, data_limite: str) -> list[dict[str, Any]]:
    return [
        m.model_dump() for m in buscar_termos_emergentes(_get_client(), pais, data_limite)
    ]


@mcp.tool()
def comparar_termo_tool(
    termo: str, pais: str, data_inicio: str, data_fim: str
) -> list[dict[str, Any]]:
    return [
        m.model_dump()
        for m in comparar_termo(_get_client(), termo, pais, data_inicio, data_fim)
    ]
