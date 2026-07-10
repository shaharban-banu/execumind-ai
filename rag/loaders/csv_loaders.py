"""
Generic CSV document loader.

Loads text-based documents from a canonical CSV file and converts
them into LangChain Document objects.
"""
from typing import Any
import pandas as pd
from langchain_core.documents import Document
from rag.config.loader_config import LoaderConfig
from rag.loaders.base_loader import BaseLoader
from rag.schema.schema_registry import SchemaRegistry
from utils.logger import logger

class CSVLoader(BaseLoader):
    """
    Generic CSV loader.

    Loads any canonical CSV file into LangChain Documents.
    """

    def __init__(self,config: LoaderConfig,schema_registry: SchemaRegistry,) :

        self.config = config
        self.schema_registry = schema_registry

        self._validate_config()

        self.table_schema = self.schema_registry.get_table_schema(self.config.table_name)

        self.text_column = self.table_schema.text_column

        self.metadata_columns = (self.table_schema.metadata_columns)

    def load(self) :
        """
        Load documents from CSV.
        """

        df = self._read_csv()

        documents = [self._row_to_document(row) for row in df.to_dict(orient="records")]

        logger.info("Loaded %d documents from '%s'.",len(documents),self.config.file_path,)

        return documents

    def _validate_config(self) -> None:

        if self.config.file_path is None:
            raise ValueError("CSV file path is required.")

        if self.config.table_name is None:
            raise ValueError("Table name is required.")

    def _read_csv(self):
        """
        Read CSV file.
        """

        try:

            return pd.read_csv(self.config.file_path)

        except Exception as exc:

            logger.exception("Unable to read CSV '%s'.",self.config.file_path,)

            raise RuntimeError("CSV loading failed.") from exc

    def _row_to_document(self,row: dict[str, Any],) :

        metadata = {column: row.get(column) for column in self.metadata_columns}

        metadata.update(
            {
                "source": self.config.source_name or "csv",
                "table": self.config.table_name,
                "document_type": self.config.table_name,
            }
        )

        return Document(
            page_content=row.get(self.text_column, "") or "",
            metadata=metadata,
        )