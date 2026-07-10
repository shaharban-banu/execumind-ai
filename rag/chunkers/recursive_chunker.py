"""
Recursive text chunker.
"""
from utils.logger import logger
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.chunkers.base_chunker import BaseChunker

class RecursiveChunker(BaseChunker):
    """
    Recursive text chunker.
    """

    def __init__(self,chunk_size: int = 500,chunk_overlap: int = 100,) :
        """
        Initialize chunker."""

        self.splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap,)

    def chunk(self, documents):
        chunks=self.splitter.split_documents(documents)
        logger.info("created %d chunks from %d documents",len(chunks),len(documents))
        return chunks