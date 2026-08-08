"""
canonical.py

Defines the canonical data models used after semantic mapping.
These models represent the standardized dataset independent of
the original uploaded schema.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from ingestion.models.tables import Relationship


@dataclass
class CanonicalColumn:
    """
    Represents a canonical column and its mapping
    from the source dataset.
    """

    name: str
    data_type: str

    required: bool = False

    source_table: str | None = None
    source_column: str | None = None

    mapped: bool = False

    #values: list[Any] = field(default_factory=list)
    nullable: bool = True

@dataclass
class CanonicalTable:
    """
    Represents a canonical business entity.
    """

    name: str

    columns: list[CanonicalColumn] = field(default_factory=list)

    dataframe: Any | None = None

    primary_keys: list[str] = field(default_factory=list)

    relationships: list[Relationship] = field(default_factory=list)

    row_count: int = 0


@dataclass
class DatasetCapabilities:

    capabilities: dict[str, bool] = field(default_factory=dict)

    supported_entities: list[str] = field(default_factory=list)

    missing_entities: list[str] = field(default_factory=list)

    coverage: float = 0.0


@dataclass
class CanonicalDataset:
    """
    Represents the fully standardized dataset produced by
    the Canonical Builder.
    """

    tables: list[CanonicalTable] = field(default_factory=list)
    capabilities: DatasetCapabilities | None = None
    


