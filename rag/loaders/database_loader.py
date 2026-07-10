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
from rag.schema.schema_registry import SchemaRegistry
from utils.logger import logger

class DatabaseLoader(BaseLoader):
    """
    Loads review data from supported sources.
    """
    def __init__(self,config:LoaderConfig,schema_registry: SchemaRegistry,):
        self.config=config
        self.schema_registry = schema_registry

        self._validate_config()
        # Load schema once
        self.table_schema = self.schema_registry.get_table_schema(self.config.table_name)
        self.text_column = self.table_schema["text_column"]
        self.metadata_columns = self.table_schema.get("metadata_columns",[],)

    def load(self):
        rows=self._fetch_rows()
        document=[self._row_to_documents(row) for row in rows]
        logger.info("Loaded %d documents from %s ",len(document),self.config.table_name)

        return document
    def _validate_config(self):
        if self.config.session is None:
            raise ValueError("Database session is required.")

        if not self.config.table_name:
            raise ValueError("Table name is required.")

        if not self.schema_registry.table_exists(self.config.table_name):
            raise ValueError(f"Unknown table '{self.config.table_name}'.")
        
    def _fetch_rows(self):
        query=text(f"select * from {self.config.table_name}")
        try:
            result=(self.config.session.execute(query).mappings().all())
            return list(result)
        
        except SQLAlchemyError as e:
            logger.exception("failed loading table %s",self.config.table_name)
            raise RuntimeError(f"unable to load {self.config.table_name}") from e
        
    def _row_to_documents(self,row:dict[str,Any]):
        """
        Convert one database row into a Document."""
    
        return Document(page_content=row.get(self.text_column,"") or "",
                        metadata=self._build_metadata(row))
    
    def _build_metadata(self,row:dict[str,Any]):
        """build document metadata"""
        metadata = {column: row.get(column) for column in self.metadata_columns}

        metadata.update(
            {
                "document_type": self.config.table_name,
                "table": self.config.table_name,
                "source": self.config.source_name or "database",
            }
        )

        return metadata


