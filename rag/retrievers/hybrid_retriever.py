"""
Hybrid retriever.

Combines semantic and keyword retrieval.
"""
from utils.logger import logger
from langchain_core.documents import Document
from rag.retrievers.base_retriever import BaseRetriever

class HybridRetriever(BaseRetriever):
    """
    Hybrid retriever combining semantic and BM25 retrieval.
    """
    def __init__(self,semantic_retriever: BaseRetriever,bm25_retriever: BaseRetriever,) :
        """
        Initialize HybridRetriever.
        """
        self.semantic_retriever = semantic_retriever
        self.bm25_retriever = bm25_retriever

    def retrieve(self,query:str,top_k:int=20,):
        """
        Retrieve documents using hybrid search."""

        semantic_results=self.semantic_retriever.retrieve(query=query,top_k=top_k,)
        bms5_results=self.bm25_retriever.retrieve(query=query,top_k=top_k,)
        merged=semantic_results+bms5_results
        unique_documents=[]
        seen=set()
        for doc in merged:
            key=(
                doc.metadata.get("table"),
                doc.metadata.get("review_id"),
                doc.metadata.get("page"),
                doc.page_content,
            )
            if key in seen:
                continue
            seen.add(key)
            unique_documents.append(doc)
        logger.info("Hybrid retrieval returned %d unique documents",len(unique_documents),)
        return unique_documents[:top_k]