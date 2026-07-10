"""
Schema Registry for the Unified RAG Pipeline.

Loads the canonical schema and provides helper methods for
retrieving table metadata.
"""
from pathlib import Path
from typing import Any
import yaml

class SchemaRegistry:
    """
    Registry for the canonical schema.

    This class provides metadata about canonical tables,
    such as the text column and metadata columns required
    by document loaders.
    """
    def __init__(self, schema_path: Path):
        """
        Initialize the registry.

        Args:
            schema_path: Path to canonical_schema.yaml
        """
        self.schema_path = schema_path
        self.schema = self._load_schema()

    def _load_schema(self) :
        """
        Load the YAML schema.

        Returns:
            Parsed schema dictionary.
        """
        with open(self.schema_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    
    def table_exists(self, table_name: str) :
        """
        Check if a table exists.
        """
        return table_name in self.schema["tables"]

    def get_table_schema(self, table_name: str):
        """
        Return schema for one table.
        """
        if not self.table_exists(table_name):
            raise ValueError(f"Unknown table: {table_name}")

        return self.schema["tables"][table_name]

    def get_text_column(self, table_name: str) -> str:
        """
        Return the document text column.
        """
        table = self.get_table_schema(table_name)

        text_column = table.get("text_column")

        if text_column is None:
            raise ValueError(f"No text column defined for '{table_name}'.")

        return text_column

    def get_metadata_columns(self,table_name: str,) :
        """
        Return metadata columns.
        """
        table = self.get_table_schema(table_name)

        return table.get("metadata_columns", [])

    def get_primary_keys(self,table_name: str,) :
        """
        Return primary keys.
        """
        table = self.get_table_schema(table_name)

        return table.get("primary_keys", [])

    def is_optional(self,table_name: str,) :
        """
        Return whether a table is optional.
        """
        table = self.get_table_schema(table_name)

        return not table.get("required", True)
