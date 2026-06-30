class BigQueryError(Exception):
    """Raised when a BigQuery query fails."""

class InvalidCountryError(Exception):
    """Raised when an unsupported country code is provided."""

class NoDataError(Exception):
    """Raised when a query returns no results for the given parameters."""
