"""
Database document Loader.

Loads customer reviews from SQLite or CSV and converts them
into LangChain Document objects.
"""
from typing import Any
from langchain_core.documents import Document
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from rag.config.loader_config import LoaderConfig
from rag.loaders.base_loader import BaseLoader
from rag.registry import RAG_TABLES

from utils.logger import logger

class DatabaseLoader(BaseLoader):
    """
    Database document loader.

    Loads records from a configured database table and
    converts them into LangChain Document objects.
    """
    def __init__(self,config:LoaderConfig):
        """
        Initialize the database loader.

        Args:
            config: Configuration describing the database
                connection and table.

        Raises:
            ValueError:
                If the loader configuration is invalid.
        """
        self.config=config

        self._validate_config()
        
        table_config=RAG_TABLES[self.config.table_name]
        self.text_column = table_config.text_column
        self.metadata_columns = table_config.metadata_columns

    def load(self):
        """
        Load documents from the configured database table.

        Returns:
            List of LangChain Document objects.
        """
        rows=self._fetch_rows()
        document=[self._row_to_documents(row) for row in rows]
        logger.info("Loaded %d documents from %s ",len(document),self.config.table_name)

        return document
    def _validate_config(self):
        """
        Validate the loader configuration.

        Raises:
            ValueError:
                If the database session or table name
                is missing or unsupported.
        """
        if self.config.session is None:
            raise ValueError("Database session is required.")

        if not self.config.table_name:
            raise ValueError("Table name is required.")

        if self.config.table_name not in RAG_TABLES:
            raise ValueError(f"Unsupported RAG table: {self.config.table_name}")
        
    def _fetch_rows(self):
        """
        Retrieve rows from the configured database table.

        Returns:
            List of database records.

        Raises:
            RuntimeError:
                If the database query fails.
        """
        columns=[self.text_column,*self.metadata_columns,]

        query = text(f"""
            SELECT {", ".join(columns)}
            FROM {self.config.table_name}
            WHERE user_id = :user_id
        """)
        try:
            result = (
                self.config.session.execute(
                    query,
                    {"user_id": self.config.user_id},
                )
                .mappings()
                .all()
            )
            return list(result)

        except SQLAlchemyError as e:
            logger.exception("Failed loading table %s", self.config.table_name)
            raise RuntimeError(
                f"Unable to load {self.config.table_name}"
            ) from e
        
    def _row_to_documents(self,row:dict[str,Any]):
        """
        Convert a database row into a LangChain Document.

        Args:
            row: Database record.

        Returns:
            LangChain Document containing page content
            and metadata.
        """
            
        return Document(page_content=row.get(self.text_column,"") or "",
                        metadata=self._build_metadata(row))
    
    def _build_metadata(self,row:dict[str,Any]):
        """
        Build document metadata.

        Args:
            row: Database record.

        Returns:
            Metadata dictionary for the document.
        """
        metadata = {column: row.get(column) for column in self.metadata_columns}

        metadata.update(
            {
                "document_type": self.config.table_name,
                "table": self.config.table_name,
                "source": self.config.source_name or "database",
            }
        )

        return metadata


