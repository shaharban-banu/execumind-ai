"""
Index service.

Builds and reloads the RAG knowledge index from
configured data sources.
"""
from pathlib import Path
from utils.logger import logger
from database.database import SessionLocal
from rag.builder import RAGPipelineBuilder
from rag.config.loader_config import LoaderConfig
from rag.config.rag_config import load_rag_config
from rag.services.pipeline_service import create_pipeline

class IndexService:
    """
    Service for building and reloading the RAG index.
    """
    def build_index(self):
        """
        Build the RAG knowledge index.

        Loads all configured knowledge sources, rebuilds the
        vector index, reloads the active pipeline, and returns
        the build status.

        Returns:
            Dictionary containing the build result.

        Raises:
            RuntimeError:
                If index creation fails.
        """
        print("=" * 50)
        print("BUILD INDEX CALLED")
        print("=" * 50)
        logger.info("Starting knowledge index build.")

        rag_config=load_rag_config()
        # Remove existing index files
        if rag_config.index_path.exists():
            rag_config.index_path.unlink()

        if rag_config.metadata_path.exists():
            rag_config.metadata_path.unlink()

        session = SessionLocal()

        try:

            loader_configs = []

            # Database reviews
            loader_configs.append(
                LoaderConfig(
                    source_type="database",
                    source_name="reviews",
                    session=session,
                    table_name="reviews",
                )
            )

            # Business documents
            docs_dir = Path("data/uploads")

            for pdf in docs_dir.glob("*.pdf"):
                loader_configs.append(
                    LoaderConfig(
                        source_type="pdf",
                        source_name="business_document",
                        file_path=pdf,
                    )
                )

            for md in docs_dir.glob("*.md"):
                loader_configs.append(
                    LoaderConfig(
                        source_type="markdown",
                        source_name="business_document",
                        file_path=md,
                    )
                )

            logger.info(
                "Discovered %d knowledge sources.",
                len(loader_configs),
            )

            pipeline = RAGPipelineBuilder(
                rag_config=rag_config,
                loader_configs=loader_configs,
            ).build()

            documents = []

            for loader in pipeline.loaders:
                loaded = loader.load()
                documents.extend(loaded)

            if not documents:
                return {
                    "success": False,
                    "message": "No knowledge sources available for indexing."
                }

            business_document_count = max(0, len(loader_configs) - 1)

            logger.info(
                "Discovered %d business documents and 1 review source.",
                business_document_count,
            )

            pipeline.build_index()
            logger.info(
                "Knowledge index built successfully."
            )
            # Reload the newly created index
            logger.info(
                "Reloading RAG pipeline."
            )
            self.reload_pipeline()

            return {
                "success": True,
                "documents": business_document_count,
                "message": (
                    "Platform processed successfully."
                    if business_document_count == 0
                    else "Knowledge index generated successfully."
                )
            }
        except Exception as exc:
            logger.exception(
                "Failed to build knowledge index."
            )
            raise RuntimeError(
                "Knowledge index build failed."
            ) from exc

        finally:
            session.close()

    def reload_pipeline(self):
        """
        Reload the active RAG pipeline.

        Creates a new pipeline instance using the latest
        vector index.
        """
        self.pipeline = create_pipeline()