"""
Semantic retriever.
"""

from langchain_core.documents import Document

from rag.embedders.base_embedder import BaseEmbedder
from rag.retrievers.base_retriever import BaseRetriever
from rag.vectorstores.base_vectorstore import BaseVectorStore
from utils.logger import logger

class SemanticRetriever(BaseRetriever):
    """
    Semantic retriever using vector similarity.
    """
    def __init__(self,embedder: BaseEmbedder,vector_store: BaseVectorStore,) -> None:
        """
        Initialize the semantic retriever.

        Args:
            embedder: Embedding model used to encode queries.
            vector_store: Vector store used for similarity search.
        """
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self,query: str,top_k: int = 5,):
        """
        Retrieve documents using semantic similarity search.

        Args:
            query: User query.
            top_k: Maximum number of documents to return.

        Returns:
            List of retrieved LangChain Document objects.
        """

        query_embedding = self.embedder.embed([query])[0]

        results = self.vector_store.search(query_embedding,top_k,)

        logger.info(
            "Semantic retrieval returned %d documents.",
            len(results),
        )

        return results
