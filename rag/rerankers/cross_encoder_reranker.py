"""
CrossEncoder reranker.
"""
from utils.logger import logger
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder
from rag.rerankers.base_reranker import BaseReranker

class CrossEncoderReranker(BaseReranker):
    """
    CrossEncoder-based reranker.
    """

    def __init__(self,model_name: str,):
        """
        Initialize the CrossEncoder reranker.

        Args:
            model_name: Name or path of the CrossEncoder model.
        """
        self.model=CrossEncoder(model_name)
        logger.info("Loaded reranker model '%s'.",model_name)
    
    def rerank(self,query:str,documents:list[Document],top_k:int=5):
        """
        Rerank retrieved documents using a CrossEncoder model.

        Args:
            query: User query.
            documents: Retrieved documents to rerank.
            top_k: Number of top-ranked documents to return.

        Returns:
            List of reranked LangChain Document objects.
        """

        if not documents:
            return []
        pairs=[
            (query,document.page_content)
              for document in documents]
        scores=self.model.predict(pairs)
        ranked=sorted(
            zip(documents,scores),
            key=lambda i:i[1],
            reverse=True)
        reranked=[document for document ,_ in ranked[:top_k]]

        logger.info("Reranked %d documents",len(documents))
        return reranked