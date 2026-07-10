"""
Factory for creating document loaders.
"""
from rag.config.loader_config import LoaderConfig
from rag.loaders.base_loader import BaseLoader
from rag.loaders.csv_loaders import CSVLoader
from rag.loaders.database_loader import DatabaseLoader
from rag.loaders.markdown_loader import MarkdownLoader
from rag.loaders.pdf_loader import PDFLoader
from rag.schema.schema_registry import SchemaRegistry

class LoaderFactory:
    """
    Factory class for creating document loaders.
    """
    @staticmethod
    def create_loader(config: LoaderConfig,schema_registry: SchemaRegistry | None = None,) :
        """
        Create the appropriate loader."""
        source_type = config.source_type.lower()

        if source_type == "database":
            if schema_registry is None:
                raise ValueError("SchemaRegistry is required for database loader.")
            return DatabaseLoader(config,schema_registry,)
        
        if source_type == "csv":
            if schema_registry is None:
                raise ValueError("SchemaRegistry is required for CSV loader.")
            return CSVLoader(config,schema_registry,)
        
        if source_type == "pdf":
            return PDFLoader(config)
        
        if source_type == "markdown":
            return MarkdownLoader(config)
        
        raise ValueError(f"unsupported sorce type {config.source_type}")