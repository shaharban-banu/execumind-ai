"""
Custom exceptions for the ETL pipeline.
"""


class ETLError(Exception):
    """Base exception for ETL."""


class DatasetValidationError(ETLError):
    """Raised when dataset validation fails."""


class SchemaMappingError(ETLError):
    """Raised when schema mapping fails."""


class ConnectorError(ETLError):
    """Raised when connector fails."""