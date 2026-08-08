"""
unmapped.py

Models for tables that could not be mapped to the canonical schema.
"""

from dataclasses import dataclass


@dataclass
class UnmappedTable:
    """
    Represents an uploaded table that is not part of the
    canonical business schema.
    """

    table_name: str

    confidence: float

    reason: str

    suggested_entity: str | None = None