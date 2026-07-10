"""
PDF document loader.

Loads PDF documents and converts them into LangChain
Document objects.
"""
import fitz
from langchain_core.documents import Document

from rag.config.loader_config import LoaderConfig
from rag.loaders.base_loader import BaseLoader
from utils.logger import logger

class PDFLoader(BaseLoader):
    """
    Loader for PDF documents.
    """

    def __init__(self, config: LoaderConfig):
        self.config=config
        self._validate_config()
    
    def load(self):
        documents: list[Document] = []
        try:

            pdf = fitz.open(self.config.file_path)
            for page_number, page in enumerate(pdf):
                text = page.get_text().strip()
                if not text:
                    continue

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": self.config.source_name or "pdf",
                            "document_type": "pdf",
                            "file_name": self.config.file_path.name,
                            "page": page_number + 1,
                        },
                    )
                )

            pdf.close()

            logger.info("Loaded %d pages from '%s'.",len(documents),self.config.file_path.name,)
            return documents

        except Exception as exc:

            logger.exception("Failed loading PDF '%s'.",self.config.file_path,)

            raise RuntimeError("Unable to load PDF.") from exc
    def _validate_config(self) -> None:
        """
        Validate configuration.
        """

        if self.config.file_path is None:
            raise ValueError("PDF file path is required.")