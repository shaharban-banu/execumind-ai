"""
BM25 keyword retriever.
"""
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi
from utils.logger import logger
from rag.retrievers.base_retriever import BaseRetriever
from utils.tokeniser import tokenize

class BM25Retriever(BaseRetriever):
    """
    Keyword-based BM25 retriever.
    """

    def __init__(self,documents: list[Document],) :
        """
        Initialize BM25 index.

        Args:
            documents: Documents to index for keyword retrieval.
        """
        self.documents=documents
        self.corpus=[
            tokenize(document.page_content) 
            for document in documents]
        self.bm25=BM25Okapi(self.corpus)
        logger.info("BM25 index create with %d documents",len(documents))

    def retrieve(self,query:str,top_k:int=5):
        """
        Retrieve the most relevant documents using BM25.

        Args:
            query: User query.
            top_k: Maximum number of documents to return.

        Returns:
            List of retrieved LangChain Document objects.
        """
        query_tokens=tokenize(query)

        scores=self.bm25.get_scores(query_tokens)

        ranked=sorted(
            zip(self.documents,scores),
            key=lambda i:i[1],
            reverse=True)
        result=[document for document,_ in ranked[:top_k]]
        logger.info("Retrievd %d BM25 documents",len(result))
        return result
