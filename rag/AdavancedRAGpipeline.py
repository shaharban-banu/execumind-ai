"""
Advanced RAG Pipeline.

Coordinates the complete Retrieval-Augmented Generation workflow.
"""

from utils.logger import logger
from pathlib import Path
from rag.chunkers.base_chunker import BaseChunker
from rag.embedders.base_embedder import BaseEmbedder
from rag.loaders.base_loader import BaseLoader
from rag.preprocessors.base_preprocessor import BasePreprocessor
from rag.rerankers.base_reranker import BaseReranker
from rag.retrievers.base_retriever import BaseRetriever
from rag.vectorstores.base_vectorstore import BaseVectorStore
from rag.retrievers.semantic_retriever import SemanticRetriever
from rag.retrievers.bm25_retriever import BM25Retriever
from rag.retrievers.hybrid_retriever import HybridRetriever
from rag.config.rag_config import RAGConfig

class AdvancedRAGPipeline:
    """
    Advanced Retrieval-Augmented Generation pipeline.

    Coordinates document loading,
    preprocessing,
    indexing and retrieval.
    """
    
    def __init__(
        self,
        loaders: list[BaseLoader],
        preprocessor: BasePreprocessor,
        chunker: BaseChunker,
        embedder: BaseEmbedder,
        vector_store: BaseVectorStore,
        retriever: BaseRetriever,
        rag_config: RAGConfig,
        reranker: BaseReranker | None = None,
        
    ):
        self.loaders = loaders
        self.preprocessor = preprocessor
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store

        self.retriever = retriever
        self.reranker = reranker
        self.rag_config = rag_config

    def initialize(self):
        """
        Initialize the vector store.

        Build the index if it doesn't exist,
        otherwise load the existing index.
        """

        if (
            not self.vector_store.index_path.exists()
            or not self.vector_store.metadata_path.exists()
        ):
            logger.info("No existing index found. Building a new index...")
            self.build_index()

        self.load_index()

    def build_index(self):
        """
        Build vector index.
        """

        logger.info("Starting index build...")

        documents = []

        for loader in self.loaders:

            loaded = loader.load()

            logger.info(
                "Loaded %d documents from %s",
                len(loaded),
                loader.__class__.__name__,
            )

            documents.extend(loaded)

        documents = self.preprocessor.process(documents)

        chunks = self.chunker.chunk(documents)

        logger.info(
            "Generated %d chunks.",
            len(chunks),
        )

        texts = [
            chunk.page_content
            for chunk in chunks
        ]

        embeddings = self.embedder.embed(texts)

        logger.info(
            "Generated %d embeddings.",
            len(embeddings),
        )

        self.vector_store.build(
            documents=chunks,
            embeddings=embeddings,
        )

        self.vector_store.save()

        logger.info("Index build completed.")

    def load_index(self):
        """
        Load FAISS index.
        """

        logger.info("Loading vector index...")

        self.vector_store.load()
        self.prepare_for_querying()

        logger.info("Vector index loaded.")

    def retrieve(
        self,
        query: str,
        retrieval_top_k: int| None = None,
        rerank_top_k: int | None = None,
    ):
        """
        Retrieve relevant documents.
        """

        logger.info(
            "Retrieving documents..."
        )

        retrieval_top_k = (retrieval_top_k or self.rag_config.retrieval_top_k)
        rerank_top_k = (rerank_top_k or self.rag_config.rerank_top_k)

        documents = self.retriever.retrieve(
            query=query,
            top_k=retrieval_top_k,
        )

        logger.info(
            "Retrieved %d documents.",
            len(documents),
        )

        if self.reranker:

            documents = self.reranker.rerank(
                query=query,
                documents=documents,
                top_k=rerank_top_k,
            )

            logger.info(
                "Returning %d reranked documents.",
                len(documents),
            )

        return documents
    
    def prepare_for_querying(self) -> None:
        """
        Prepare the pipeline for retrieval.
        """

        if not hasattr(self.vector_store, "documents"):
            raise RuntimeError(
                "Vector store must be loaded before preparing the pipeline."
            )

        documents = self.vector_store.documents

        semantic = SemanticRetriever(
            embedder=self.embedder,
            vector_store=self.vector_store,
        )

        bm25 = BM25Retriever(
            documents=documents,
        )

        self.retriever = HybridRetriever(
            semantic_retriever=semantic,
            bm25_retriever=bm25,
        )