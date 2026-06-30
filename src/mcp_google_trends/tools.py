from typing import cast

from google.cloud import bigquery

from .bigquery_client import BQ_DATASET, run_query
from .exceptions import InvalidCountryError
from .models import RisingTerm, TermComparison, TrendingTerm

VALID_COUNTRIES = {"BR", "US", "GB", "DE", "FR", "JP", "IN", "CA", "AU", "ES"}


def _validate_pais(pais: str) -> str:
    code = pais.upper()
    if code not in VALID_COUNTRIES:
        raise InvalidCountryError(
            f"Unsupported country '{pais}'. "
            f"Valid codes: {', '.join(sorted(VALID_COUNTRIES))}"
        )
    return code


def _to_trending(row: dict[str, object]) -> TrendingTerm:
    return TrendingTerm(
        term=cast(str, row["term"]),
        score=cast(int | None, row.get("score")),
        rank=cast(int, row["rank"]),
    )


def _to_rising(row: dict[str, object]) -> RisingTerm:
    return RisingTerm(
        term=cast(str, row["term"]),
        percent_gain=cast(int, row["percent_gain"]),
        score=cast(int | None, row.get("score")),
    )


def _to_comparison(row: dict[str, object]) -> TermComparison:
    return TermComparison(
        week=cast(str, row["week"]),
        term=cast(str, row["term"]),
        score=cast(int | None, row.get("score")),
        rank=cast(int, row["rank"]),
    )


def buscar_termos_em_alta(
    client: bigquery.Client,
    pais: str,
    data_limite: str,
) -> list[TrendingTerm]:
    pais_code = _validate_pais(pais)
    sql = f"""
        SELECT term, score, rank
        FROM `{BQ_DATASET}.international_top_terms`
        WHERE country_code = @country_code
          AND week >= @date_threshold
        ORDER BY week DESC, rank ASC
    """
    rows = run_query(client, sql, {"country_code": pais_code, "date_threshold": data_limite})
    return [_to_trending(row) for row in rows]


def buscar_termos_emergentes(
    client: bigquery.Client,
    pais: str,
    data_limite: str,
) -> list[RisingTerm]:
    pais_code = _validate_pais(pais)
    sql = f"""
        SELECT term, percent_gain, score
        FROM `{BQ_DATASET}.international_top_rising_terms`
        WHERE country_code = @country_code
          AND week >= @date_threshold
        ORDER BY percent_gain DESC
    """
    rows = run_query(client, sql, {"country_code": pais_code, "date_threshold": data_limite})
    return [_to_rising(row) for row in rows]


def comparar_termo(
    client: bigquery.Client,
    termo: str,
    pais: str,
    data_inicio: str,
    data_fim: str,
) -> list[TermComparison]:
    pais_code = _validate_pais(pais)
    sql = f"""
        SELECT CAST(week AS STRING) AS week, term, score, rank
        FROM `{BQ_DATASET}.international_top_terms`
        WHERE country_code = @country_code
          AND LOWER(term) = @term
          AND week BETWEEN @start_date AND @end_date
        ORDER BY week ASC
    """
    rows = run_query(
        client,
        sql,
        {
            "country_code": pais_code,
            "term": termo.lower(),
            "start_date": data_inicio,
            "end_date": data_fim,
        },
    )
    return [_to_comparison(row) for row in rows]
