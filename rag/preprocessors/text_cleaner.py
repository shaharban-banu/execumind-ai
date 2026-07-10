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
    Preprocess documents before chunking.
    """
    def process(self,documents: list[Document],) :
        """
        Preprocess documents."""
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
        return unicodedata.normalize("NFKC", text)

    @staticmethod
    def _normalize_line_endings(text: str) -> str:
        return text.replace("\r\n", "\n").replace("\r", "\n")

    @staticmethod
    def _remove_extra_whitespace(text: str) -> str:
        return re.sub(r"[ \t]+", " ", text)

    @staticmethod
    def _remove_empty_lines(text: str) -> str:
        return re.sub(r"\n{3,}", "\n\n", text)

    @staticmethod
    def _remove_boilerplate(text: str) -> str:
        """
        Remove common PDF artifacts.
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