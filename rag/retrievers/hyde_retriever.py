"""
HyDE Retriever.
"""

from langchain_core.documents import Document
from utils.logger import logger
from rag.embedders.base_embedder import BaseEmbedder
from rag.retrievers.base_retriever import BaseRetriever
from rag.vectorstores.base_vectorstore import BaseVectorStore

class HyDERetriever(BaseRetriever):
    """Hypothetical Document Embeddings Retriever."""
    def __init__(self,llm,embedder:BaseEmbedder,vector_store:BaseVectorStore,):
        """initialise HyDE retriever"""

        self.llm=llm
        self.embedder=embedder
        self.vector_store=vector_store
    
    def retrieve(self,query:str,top_k:int=5,):
        """ Retrieve documents using HyDE."""

        hypothetical_document=(self._generate_hypothetical_document(query))
        embedding=self.embedder.embed([hypothetical_document])[0]
        return self.vector_store.search(embedding,top_k,)
    def _generate_hypothetical_document(self,query:str,):
        """
        Generate hypothetical answer.
        """
        prompt=f"""Generate a detailed document that would answer the following question.
        Question:
        {query}
        Document:
        """
        response=self.llm.invoke(prompt)
        logger.info("Generated hypothetical document")
        return response.content




