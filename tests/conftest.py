from unittest.mock import patch

import pytest


@pytest.fixture
def mock_bigquery_client():
    with patch("mcp_google_trends.tools.run_query") as mock:
        yield mock
