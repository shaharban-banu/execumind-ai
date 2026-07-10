"""
Builds the complete Advanced RAG Pipeline.
"""

from rag.config.loader_config import LoaderConfig
from rag.config.rag_config import RAGConfig
from rag.preprocessors.text_cleaner import DocumentPreprocessor
from rag.chunkers.recursive_chunker import RecursiveChunker
from rag.embedders.sentence_transformer_embedder import (SentenceTransformerEmbedder,)
from rag.vectorstores.faiss_vectorstore import FAISSStore
from rag.loaders.loader_factory import LoaderFactory
from rag.loaders.base_loader import BaseLoader
from rag.rerankers.cross_encoder_reranker import (CrossEncoderReranker,)

# from rag.retrievers.semantic_retriever import SemanticRetriever
# from rag.retrievers.bm25_retriever import BM25Retriever
# from rag.retrievers.hybrid_retriever import HybridRetriever
# from rag.retrievers.hyde_retriever import HyDERetriever
from rag.AdavancedRAGpipeline import AdvancedRAGPipeline
from rag.schema.schema_registry import SchemaRegistry

class RAGPipelineBuilder:
    """
    Builder for the Advanced RAG Pipeline.
    """

    def __init__(
        self,
        rag_config: RAGConfig,
        loader_configs: list[LoaderConfig],
        schema_registry: SchemaRegistry,
    ):
        self.rag_config = rag_config
        self.loader_configs = loader_configs
        self.schema_registry = schema_registry
    def build(self):
        """
        Build the complete RAG pipeline.
        """
        loaders = self._build_loaders()
        preprocessor = self._build_preprocessor()
        chunker = self._build_chunker()
        embedder = self._build_embedder()
        vector_store = self._build_vector_store()
        reranker = self._build_reranker()

        return AdvancedRAGPipeline(
            loaders=loaders,
            preprocessor=preprocessor,
            chunker=chunker,
            embedder=embedder,
            vector_store=vector_store,
            rag_config=self.rag_config,
            retriever=None,
            reranker=reranker,
        )

    def _build_preprocessor(self):
        """
        Build the document preprocessor.
        """
        return DocumentPreprocessor()
    def _build_chunker(self):
        """
        Build the document chunker.
        """
        return RecursiveChunker(
            chunk_size=self.rag_config.chunk_size,
            chunk_overlap=self.rag_config.chunk_overlap,
        )
    def _build_embedder(self):
        """
        Build the embedding model.
        """
        return SentenceTransformerEmbedder(model_name=self.rag_config.embedding_model,)
    def _build_vector_store(self):
        """
        Build the vector store.
        """
        return FAISSStore(
            index_path=self.rag_config.index_path,
            metadata_path=self.rag_config.metadata_path,
        )
    def _build_loaders(self) -> list[BaseLoader]:
        """
        Build all configured loaders.
        """

        loaders = []

        for config in self.loader_configs:

            loader = LoaderFactory.create_loader(
                config=config,
                schema_registry=self.schema_registry,
            )
            loaders.append(loader)
        return loaders
    
    def _build_reranker(self):
        """
        Build the reranker.
        """
        return CrossEncoderReranker(model_name=self.rag_config.reranker_model,)
    
    # def _build_retrievers(self,embedder,vector_store,documents,llm=None,):
    #     """
    #     Build all retrievers."""
    #     semantic=SemanticRetriever(embedder=embedder,vector_store=vector_store)
    #     bm25=BM25Retriever(documents=documents)
    #     hybrid=HybridRetriever(semantic_retriever=semantic,bm25_retriever=bm25)
    #     hyde=HyDERetriever(llm=llm,embedder=embedder,vector_store=vector_store)

    #     return {
    #         "semantic":semantic,
    #         "bm25":bm25,
    #         "hybrid":hybrid,
    #         "hyde":hyde,
    #     }
