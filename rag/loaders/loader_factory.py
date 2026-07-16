"""
Factory for creating document loaders.
"""
from rag.config.loader_config import LoaderConfig
from rag.loaders.csv_loaders import CSVLoader
from rag.loaders.database_loader import DatabaseLoader
from rag.loaders.markdown_loader import MarkdownLoader
from rag.loaders.pdf_loader import PDFLoader


class LoaderFactory:
    """
    Factory class for creating document loaders.
    """
    @staticmethod
    def create_loader(config: LoaderConfig) :
        """
        Create the appropriate loader."""
        source_type = config.source_type.lower()

        if source_type == "database":
            
            return DatabaseLoader(config)
        
        if source_type == "csv":
            
            return CSVLoader(config)
        
        if source_type == "pdf":
            return PDFLoader(config)
        
        if source_type == "markdown":
            return MarkdownLoader(config)
        
        raise ValueError(f"unsupported sorce type {config.source_type}")