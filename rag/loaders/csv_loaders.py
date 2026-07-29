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
from rag.registry import RAG_TABLES
from utils.logger import logger

class CSVLoader(BaseLoader):
    """
    Generic CSV loader.

    Loads any canonical CSV file into LangChain Documents.
    """

    def __init__(self,config: LoaderConfig) :
        """
        Initialize the CSV loader.

        Args:
            config: Configuration describing the CSV source
                and table metadata.

        Raises:
            ValueError:
                If the configuration is invalid or the table
                is not registered for RAG.
        """

        self.config = config

        self._validate_config()

        if self.config.table_name not in RAG_TABLES:
            raise ValueError(
                f"Table '{self.config.table_name}' is not configured for RAG."
            )

        table = RAG_TABLES[self.config.table_name]

        self.text_column = table.text_column
        self.metadata_columns = table.metadata_columns

    def load(self) :
        """
        Load documents from a CSV file.

        Reads the configured CSV file and converts each row
        into a LangChain Document.

        Returns:
            List of loaded documents.
        """

        df = self._read_csv()

        documents = [self._row_to_document(row) for row in df.to_dict(orient="records")]

        logger.info("Loaded %d documents from '%s'.",len(documents),self.config.file_path,)

        return documents

    def _validate_config(self) -> None:
        """
        Validate the loader configuration.

        Raises:
            ValueError:
                If the file path or table name is missing.
        """

        if self.config.file_path is None:
            raise ValueError("CSV file path is required.")

        if self.config.table_name is None:
            raise ValueError("Table name is required.")

    def _read_csv(self):
        """
        Read the configured CSV file.

        Returns:
            DataFrame containing the CSV contents.

        Raises:
            RuntimeError:
                If the CSV file cannot be loaded.
        """

        try:

            return pd.read_csv(self.config.file_path)

        except Exception as exc:

            logger.exception("Unable to read CSV '%s'.",self.config.file_path,)

            raise RuntimeError("CSV loading failed.") from exc

    def _row_to_document(self,row: dict[str, Any],) :
        """
        Convert a CSV row into a LangChain Document.

        Args:
            row: Dictionary representing a CSV record.

        Returns:
            LangChain Document containing the row content
            and metadata.
        """

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