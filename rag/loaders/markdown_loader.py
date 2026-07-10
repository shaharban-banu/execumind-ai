"""
Markdown document loader.

Loads Markdown documents and converts them into LangChain
Document objects.
"""

from __future__ import annotations

import logging

from langchain_core.documents import Document

from rag.config.loader_config import LoaderConfig
from rag.loaders.base_loader import BaseLoader

logger = logging.getLogger(__name__)


class MarkdownLoader(BaseLoader):
    """
    Loader for Markdown documents.
    """

    def __init__(self, config: LoaderConfig) -> None:
        """
        Initialize Markdown loader.

        Args:
            config: Loader configuration.
        """
        self.config = config
        self._validate_config()

    def load(self) -> list[Document]:
        """
        Load Markdown document.

        Returns:
            List of Document objects.
        """
        try:

            text = self.config.file_path.read_text(
                encoding="utf-8"
            )

            document = Document(
                page_content=text,
                metadata={
                    "source": self.config.source_name or "markdown",
                    "document_type": "markdown",
                    "file_name": self.config.file_path.name,
                },
            )

            logger.info(
                "Loaded markdown file '%s'.",
                self.config.file_path.name,
            )

            return [document]

        except Exception as exc:

            logger.exception(
                "Failed loading markdown '%s'.",
                self.config.file_path,
            )

            raise RuntimeError(
                "Unable to load markdown file."
            ) from exc

    def _validate_config(self) -> None:
        """
        Validate configuration.
        """
        if self.config.file_path is None:
            raise ValueError(
                "Markdown file path is required."
            )