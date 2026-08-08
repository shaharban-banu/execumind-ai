"""
table.py

Defines the core metadata models used throughout the ingestion pipeline.
These models represent dataset tables, columns, and detected relationships.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ColumnMetadata:
    """
    Represents metadata for a single column in a table.
    """

    name: str
    data_type: str
    null_percentage: float
    unique_count: int
    sample_values: list[Any] = field(default_factory=list)
    is_primary_key: bool = False
    is_foreign_key: bool = False
    is_nullable: bool = True


@dataclass
class Relationship:
    """
    Represents a detected relationship between two tables.
    """

    source_table: str
    source_column: str
    target_table: str
    target_column: str
    canonical_column: str
    relationship_type: str = "foreign_key"
    confidence: float = 0.0


@dataclass
class TableMetadata:
    """
    Represents metadata for a dataset table.
    """

    table_name: str
    columns: list[ColumnMetadata] = field(default_factory=list)
    row_count: int = 0
    dataframe: Any | None = None
    primary_keys: list[str] = field(default_factory=list)
    foreign_keys: list[str] = field(default_factory=list)