"""
Common setup for RAG tests.
"""

from pathlib import Path

from database.database import SessionLocal
from rag.AdavancedRAGpipeline import AdvancedRAGPipeline
from rag.builder import RAGPipelineBuilder
from rag.config.loader_config import LoaderConfig
from rag.config.rag_config import load_rag_config



def create_test_pipeline() -> AdvancedRAGPipeline:
    """
    Create a ready-to-use RAG pipeline.
    """

    session = SessionLocal()

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

    builder = RAGPipelineBuilder(
        rag_config=load_rag_config(),
        loader_configs=loader_configs,

    )

    pipeline = builder.build()

    if (
    Path(pipeline.vector_store.index_path).exists()
    and Path(pipeline.vector_store.metadata_path).exists()):
        pipeline.load_index()
    else:
        pipeline.build_index()
        pipeline.load_index()

    return pipeline