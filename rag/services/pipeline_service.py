"""
Pipeline service.

Creates and initializes the Advanced RAG pipeline
using the configured knowledge sources.
"""
from pathlib import Path
from utils.logger import logger
from database.database import SessionLocal
from rag.AdavancedRAGpipeline import AdvancedRAGPipeline
from rag.builder import RAGPipelineBuilder
from rag.config.loader_config import LoaderConfig
from rag.config.rag_config import load_rag_config
from rag.services.user_paths import get_user_vectorstore_paths

def create_pipeline(user_id:int) -> AdvancedRAGPipeline:
    """
    Create and initialize the RAG pipeline.

    Builds the pipeline from the configured knowledge
    sources and loads the existing vector index if
    available.

    Returns:
        A fully initialized AdvancedRAGPipeline instance.

    Raises:
        RuntimeError:
            If pipeline creation fails.
    """

    session = SessionLocal()

    loader_configs = []

    logger.info("Creating RAG pipeline.")

    try:
        # Database reviews
        loader_configs.append(
            LoaderConfig(
                source_type="database",
                source_name="reviews",
                session=session,
                table_name="reviews",
                user_id=user_id,
            )
        )

        # Business documents
        docs_dir = Path(f"data/users/{user_id}/uploads")

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

        rag_config = load_rag_config()

        index_path, metadata_path = get_user_vectorstore_paths(user_id)

        rag_config.index_path = index_path
        rag_config.metadata_path = metadata_path

        builder = RAGPipelineBuilder(
            rag_config=rag_config,
            loader_configs=loader_configs,
        )

        pipeline = builder.build()

        
        if (
            pipeline.vector_store.index_path.exists()
            and pipeline.vector_store.metadata_path.exists()
        ):
            pipeline.load_index()
        else:
            raise RuntimeError(
                "Knowledge index not found. Run Platform Process first."
            )


        return pipeline
    except RuntimeError:
        raise

    except Exception as exc:
            logger.exception(
                "Failed to create RAG pipeline."
            )
            raise RuntimeError(
                "Pipeline initialization failed."
            ) from exc

    finally:
        session.close()