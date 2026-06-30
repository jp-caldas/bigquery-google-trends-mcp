from google.cloud import bigquery

from .config import GOOGLE_CLOUD_PROJECT
from .exceptions import BigQueryError

BQ_DATASET = "bigquery-public-data.google_trends"


def create_client() -> bigquery.Client:
    return bigquery.Client(project=GOOGLE_CLOUD_PROJECT)


def _make_param(key: str, value: object) -> bigquery.ScalarQueryParameter:
    if isinstance(value, str):
        return bigquery.ScalarQueryParameter(key, "STRING", value)
    if isinstance(value, float):
        return bigquery.ScalarQueryParameter(key, "FLOAT", value)
    if isinstance(value, int):
        return bigquery.ScalarQueryParameter(key, "INT64", value)
    raise BigQueryError(f"Unsupported parameter type for '{key}': {type(value)}")


def run_query(
    client: bigquery.Client,
    sql: str,
    params: dict[str, object],
) -> list[dict[str, object]]:
    try:
        job_config = bigquery.QueryJobConfig(
            query_parameters=[_make_param(k, v) for k, v in params.items()]
        )
        results = client.query(sql, job_config=job_config).result()
        return [dict(row.items()) for row in results]
    except Exception as e:
        raise BigQueryError(f"BigQuery query failed: {e}") from e
