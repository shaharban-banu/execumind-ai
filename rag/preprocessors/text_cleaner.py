"""
Document preprocessor.

Applies text normalization to LangChain Documents.
"""
import re
import unicodedata

from langchain_core.documents import Document
from utils.logger import logger
from rag.preprocessors.base_preprocessor import BasePreprocessor

class DocumentPreprocessor(BasePreprocessor):
    """
    Document preprocessor.

    Applies text normalization and cleanup operations
    before documents are chunked.
    """
    def process(self,documents: list[Document],) :
        """
        Preprocess a collection of documents.

        Applies Unicode normalization, whitespace cleanup,
        boilerplate removal, and line normalization.
        """
        processed = []

        for document in documents:

            text = document.page_content

            text = self._normalize_unicode(text)
            text = self._normalize_line_endings(text)
            text = self._remove_boilerplate(text)
            text = self._remove_extra_whitespace(text)
            text = self._remove_empty_lines(text)
            text = text.strip()

            processed.append(
                Document(page_content=text, 
                         metadata=document.metadata.copy(),))

        logger.info("Preprocessed %d documents.",len(processed),)

        return processed

    @staticmethod
    def _normalize_unicode(text: str) -> str:
        """
        Normalize Unicode characters to NFKC form.

        Args:
            text: Input text.

        Returns:
            Normalized text.
        """
        return unicodedata.normalize("NFKC", text)

    @staticmethod
    def _normalize_line_endings(text: str) -> str:
        """
        Normalize line endings to Unix format.

        Args:
            text: Input text.

        Returns:
            Text with normalized line endings.
        """
        return text.replace("\r\n", "\n").replace("\r", "\n")

    @staticmethod
    def _remove_extra_whitespace(text: str) -> str:
        """
        Collapse consecutive spaces and tabs.

        Args:
            text: Input text.

        Returns:
            Cleaned text.
        """
        return re.sub(r"[ \t]+", " ", text)

    @staticmethod
    def _remove_empty_lines(text: str) -> str:
        """
        Reduce multiple blank lines.

        Args:
            text: Input text.

        Returns:
            Text with excessive blank lines removed.
        """
        return re.sub(r"\n{3,}", "\n\n", text)

    @staticmethod
    def _remove_boilerplate(text: str) -> str:
        """
        Remove common boilerplate patterns.

        Args:
            text: Input text.

        Returns:
            Cleaned text with common PDF artifacts removed.
        """

        patterns = [
            r"Page\s+\d+",
            r"CONFIDENTIAL",
        ]

        for pattern in patterns:
            text = re.sub(
                pattern,
                "",
                text,
                flags=re.IGNORECASE,
            )

        return text