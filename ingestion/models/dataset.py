"""
dataset.py

Defines the metadata model representing an uploaded dataset.
A dataset may contain one or more tables loaded from CSV, Excel, or JSON files.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from ingestion.models.tables import Relationship, TableMetadata
from ingestion.models.mapping import ColumnMapping, TableMapping
from ingestion.models.unmapped import UnmappedTable

@dataclass
class DatasetMetadata:
    """
    Represents an uploaded dataset and its discovered metadata.
    """

    dataset_name: str
    source_path: str
    file_type: str
    tables: list[TableMetadata] = field(default_factory=list)
    relationships: list[Relationship] = field(default_factory=list)
    discovered_at: datetime = field(default_factory=datetime.now)
    table_mappings: list[TableMapping] = field(default_factory=list)
    column_mappings: list[ColumnMapping] = field(default_factory=list)
    unmapped_tables: list[UnmappedTable] = field(default_factory=list)