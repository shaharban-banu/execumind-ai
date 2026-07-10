"""
Semantic retriever.
"""

from langchain_core.documents import Document

from rag.embedders.base_embedder import BaseEmbedder
from rag.retrievers.base_retriever import BaseRetriever
from rag.vectorstores.base_vectorstore import BaseVectorStore


class SemanticRetriever(BaseRetriever):
    """
    Semantic retriever using vector similarity.
    """
    def __init__(self,embedder: BaseEmbedder,vector_store: BaseVectorStore,) -> None:

        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self,query: str,top_k: int = 5,):
        """
        Retrieve similar documents.
        """

        query_embedding = self.embedder.embed([query])[0]

        return self.vector_store.search(query_embedding,top_k,)