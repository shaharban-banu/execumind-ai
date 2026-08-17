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
from rag.services.user_paths import get_user_vectorstore_paths

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
        """
        Initialize the Advanced RAG pipeline.

        Args:
            loaders: Document loaders.
            preprocessor: Document preprocessor.
            chunker: Document chunker.
            embedder: Embedding model.
            vector_store: Vector store implementation.
            retriever: Retrieval strategy.
            rag_config: RAG configuration.
            reranker: Optional reranker.
        """
        self.loaders = loaders
        self.preprocessor = preprocessor
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store

        self.retriever = retriever
        self.reranker = reranker
        self.rag_config = rag_config

    def initialize(self,user_id:int):
        """
        Initialize the vector store.

        Build the index if it doesn't exist,
        otherwise load the existing index.
        """
        index_path, metadata_path = get_user_vectorstore_paths(user_id)

        self.vector_store.index_path = index_path
        self.vector_store.metadata_path = metadata_path
        if (
            not self.vector_store.index_path.exists()
            or not self.vector_store.metadata_path.exists()
        ):
            logger.info("No existing index found. Building a new index...")
            self.build_index()

        self.load_index()

    def build_index(self,user_id:int):
        """
        Build vector index.

        Loads documents, preprocesses them, creates chunks,
        generates embeddings, and stores the resulting index.

        Raises:
            RuntimeError:
                If index creation fails.
        """

        logger.info("Starting index build...")

        index_path, metadata_path = get_user_vectorstore_paths(user_id)

        self.vector_store.index_path = index_path
        self.vector_store.metadata_path = metadata_path

        documents = []

        try:

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

            for i, chunk in enumerate(chunks):
                #source = chunk.metadata.get("source_name", "unknown")
                chunk.metadata["chunk_id"] = i

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

        except Exception as exc:
            logger.exception(
                "Failed to build vector index."
            )
            raise RuntimeError(
                "Vector index build failed."
            ) from exc

    def load_index(self):
        """
        Load the vector index and prepare retrievers.

        Raises:
            RuntimeError:
                If the vector store cannot be loaded.
        """

        logger.info("Loading vector index...")

        try:
            self.vector_store.load()
            self.prepare_for_querying()

            logger.info("Vector index loaded.")
            
        except Exception as exc:
            logger.exception(
                "Failed loading vector index."
            )
            raise RuntimeError(
                "Unable to load vector index."
            ) from exc

    def retrieve(
        self,
        query: str,
        user_id:int,
        retrieval_top_k: int| None = None,
        rerank_top_k: int | None = None,
    ):
        """
        Retrieve documents relevant to a query.

        Args:
            query: User query.
            retrieval_top_k: Number of documents to retrieve.
            rerank_top_k: Number of reranked documents.

        Returns:
            List of retrieved documents.
        """

        logger.info(
            "Retrieving documents..."
        )
        
        index_path, metadata_path = get_user_vectorstore_paths(user_id)

        self.vector_store.index_path = index_path
        self.vector_store.metadata_path = metadata_path

        self.load_index()

        retrieval_top_k = (retrieval_top_k or self.rag_config.retrieval_top_k)
        rerank_top_k = (rerank_top_k or self.rag_config.rerank_top_k)


        if self.retriever is None:
            raise RuntimeError(
                "Knowledge base is not available. Please process the platform first."
            )
        documents = self.retriever.retrieve(
            query=query,
            top_k=retrieval_top_k,
        )
        logger.info("Retrieved Documents:")

        for index, document in enumerate(documents, start=1):
            logger.info(
                "%d. Source=%s File=%s Page=%s Table=%s",
                index,
                document.metadata.get("source"),
                document.metadata.get("file_name"),
                document.metadata.get("page"),
                document.metadata.get("table"),
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
        Prepare retrieval components.

        Creates semantic, BM25, and hybrid retrievers
        using the loaded vector store.

        Raises:
            RuntimeError:
                If the vector store has not been loaded.
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

    def is_ready(self) -> bool:
        """
        Check whether the vector store is loaded.

        Returns:
            True if the pipeline is ready for querying.
        """
        return hasattr(self.vector_store, "documents")