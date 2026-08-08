"""
mapping.py

Defines models representing semantic mappings between
source dataset fields and the canonical schema.
"""
from __future__ import annotations
from dataclasses import dataclass
#from ingestion.models.canonical import CanonicalTable
from ingestion.mappings.field_types import CanonicalField


@dataclass
class ColumnMapping:
    """
    Represents a mapping between a source column and
    a canonical column.
    """

    source_table: str
    source_column: str

    canonical_entity: str
    canonical_column: str

    confidence: float
    mapping_method: str

    canonical_field: CanonicalField | None = None

    needs_confirmation: bool = False


@dataclass
class TableMapping:
    """
    Represents a mapping between a source table and
    a canonical entity.
    """

    source_table: str
    canonical_entity: str

    confidence: float
    mapping_method: str

    needs_confirmation: bool = False
    #canonical_table: CanonicalTable | None = None