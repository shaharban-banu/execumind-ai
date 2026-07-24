from pathlib import Path

from database.database import SessionLocal
from rag.AdavancedRAGpipeline import AdvancedRAGPipeline
from rag.builder import RAGPipelineBuilder
from rag.config.loader_config import LoaderConfig
from rag.config.rag_config import load_rag_config


class IndexService:

    def build_index(self):

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
        docs_dir = Path("rag/docs/uploads")

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

        pipeline = RAGPipelineBuilder(
            rag_config=load_rag_config(),
            loader_configs=loader_configs,
        ).build()

        pipeline.build_index()

        return {
            "success": True,
            "documents": len(loader_configs) - 1,# exclude reviews loader
            "message": "Knowledge index generated successfully."
        }