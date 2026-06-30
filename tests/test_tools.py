import pytest

from mcp_google_trends.exceptions import InvalidCountryError
from mcp_google_trends.models import RisingTerm, TermComparison, TrendingTerm
from mcp_google_trends.tools import (
    buscar_termos_em_alta,
    buscar_termos_emergentes,
    comparar_termo,
)


class TestBuscarTermosEmAlta:
    def test_retorna_termos_quando_encontra_dados(self, mock_bigquery_client):
        mock_bigquery_client.return_value = [
            {"term": "IA", "score": 100, "rank": 1},
            {"term": "Python", "score": 85, "rank": 2},
        ]
        resultado = buscar_termos_em_alta(mock_bigquery_client, "BR", "2024-01-01")
        assert len(resultado) == 2
        assert all(isinstance(t, TrendingTerm) for t in resultado)
        assert resultado[0].term == "IA"
        assert resultado[0].score == 100

    def test_retorna_vazio_quando_sem_dados(self, mock_bigquery_client):
        mock_bigquery_client.return_value = []
        resultado = buscar_termos_em_alta(mock_bigquery_client, "BR", "2024-01-01")
        assert resultado == []

    def test_lanca_invalid_country_error_para_codigo_invalido(self, mock_bigquery_client):
        with pytest.raises(InvalidCountryError):
            buscar_termos_em_alta(mock_bigquery_client, "XX", "2024-01-01")


class TestBuscarTermosEmergentes:
    def test_retorna_termos_quando_encontra_dados(self, mock_bigquery_client):
        mock_bigquery_client.return_value = [
            {"term": "Deep Learning", "percent_gain": 250, "score": 70},
            {"term": "Rust", "percent_gain": 150, "score": 45},
        ]
        resultado = buscar_termos_emergentes(mock_bigquery_client, "US", "2024-01-01")
        assert len(resultado) == 2
        assert all(isinstance(t, RisingTerm) for t in resultado)
        assert resultado[0].percent_gain == 250

    def test_retorna_vazio_quando_sem_dados(self, mock_bigquery_client):
        mock_bigquery_client.return_value = []
        resultado = buscar_termos_emergentes(mock_bigquery_client, "US", "2024-01-01")
        assert resultado == []


class TestCompararTermo:
    def test_retorna_series_quando_encontra_dados(self, mock_bigquery_client):
        mock_bigquery_client.return_value = [
            {"week": "2024-01-07", "term": "IA", "score": 90, "rank": 1},
            {"week": "2024-01-14", "term": "IA", "score": 95, "rank": 1},
        ]
        resultado = comparar_termo(
            mock_bigquery_client, "IA", "BR", "2024-01-01", "2024-01-31"
        )
        assert len(resultado) == 2
        assert all(isinstance(t, TermComparison) for t in resultado)
        assert resultado[0].week == "2024-01-07"

    def test_retorna_vazio_quando_sem_dados(self, mock_bigquery_client):
        mock_bigquery_client.return_value = []
        resultado = comparar_termo(
            mock_bigquery_client, "IA", "BR", "2024-01-01", "2024-01-31"
        )
        assert resultado == []
