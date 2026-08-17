from pathlib import Path
import shutil

from sqlalchemy import text

from database.database import SessionLocal
from database.models import Dataset,DatasetVersion,DatasetFile
from utils.logger import logger


class PlatformResetService:

    # MODEL_DIR = Path("data/models")
    # REPORT_DIR = Path("data/forecast_reports")
    # VECTOR_DIR = Path("data/vectorstore")

    def reset(self,user_id:int):
        """
        Clear generated intelligence artifacts.

        Used when uploading/replacing datasets.
        Does NOT clear PostgreSQL data.
        """
        logger.info("Resetting generated platform artifacts...")

        self._clear_forecast_models(user_id)
        self._clear_forecast_reports(user_id)
        self._clear_vector_store(user_id)

        logger.info("Generated platform artifacts reset completed.")

    def reset_for_reprocess(self,user_id:int):
        """
        Completely clear processed platform data while keeping:
        - uploaded datasets
        - knowledge documents

        This is used by the Reprocess Platform operation.
        """

        logger.info("Starting platform reprocess reset...")

        # 1. Clear PostgreSQL processed/business data
        self._clear_postgres_data(user_id)

        # 2. Delete generated forecast models
        self._clear_forecast_models(user_id)

        # 3. Delete generated forecast reports
        self._clear_forecast_reports(user_id)

        # 4. Delete FAISS vector store
        self._clear_vector_store(user_id)

        logger.info(
            "Platform reprocess reset completed. "
            "Datasets and knowledge documents were preserved."
        )

    def factory_reset(self,user_id:int):
        """
        Completely reset platform data and generated artifacts.

        Deletes:
        - PostgreSQL processed data
        - Uploaded datasets
        - Knowledge documents
        - FAISS vector store
        - Forecast models
        - Forecast reports

        Authentication/user data is preserved.
        """

        logger.info("Starting factory reset...")

        # 1. Clear PostgreSQL processed data
        self._clear_postgres_data(user_id)

        # 2. Delete uploaded datasets
        self._clear_directory(Path(f"data/users/{user_id}"))

        # 3. Delete knowledge documents
        self._clear_knowledge_documents(user_id)

        # 4. Delete forecast models
        self._clear_forecast_models(user_id)

        # 5. Delete forecast reports
        self._clear_forecast_reports(user_id)

        # 6. Delete FAISS vector store
        self._clear_vector_store(user_id)

        logger.info("Factory reset completed successfully.")

    def _clear_postgres_data(self,user_id:int):
        """
        Clear only processed/business tables.

        Authentication/user data is intentionally not touched.
        """

        db = SessionLocal()

        try:
            logger.info("Clearing PostgreSQL processed data...")

            db.execute(text("""
                DELETE FROM reviews
                WHERE order_id IN (
                    SELECT order_id FROM orders WHERE user_id=:uid
                )
            """), {"uid": user_id})

            db.execute(text("""
                DELETE FROM order_items
                WHERE order_id IN (
                    SELECT order_id FROM orders WHERE user_id=:uid
                )
            """), {"uid": user_id})

            db.execute(text("DELETE FROM payments WHERE user_id=:uid"), {"uid": user_id})
            db.execute(text("DELETE FROM deliveries WHERE user_id=:uid"), {"uid": user_id})
            db.execute(text("DELETE FROM orders WHERE user_id=:uid"), {"uid": user_id})
            db.execute(text("DELETE FROM customers WHERE user_id=:uid"), {"uid": user_id})
            db.execute(text("DELETE FROM sellers WHERE user_id=:uid"), {"uid": user_id})
            db.execute(text("DELETE FROM products WHERE user_id=:uid"), {"uid": user_id})
            db.execute(
                text("DELETE FROM executive_recommendations WHERE user_id = :uid"),
                {"uid": user_id},
            )


            db.commit()

            logger.info("PostgreSQL processed data cleared.")

        except Exception:
            db.rollback()
            logger.exception(
                "Failed to clear PostgreSQL processed data."
            )
            raise

        finally:
            db.close()

    def _clear_forecast_models(self,user_id:int):
        """Delete generated forecast models."""

        MODEL_DIR=Path(f"data/users/{user_id}/models")
        if not MODEL_DIR.exists():
            return

        for file in MODEL_DIR.glob("*.pkl"):
            logger.info("Removing forecast model: %s", file.name)
            file.unlink()

    def _clear_forecast_reports(self,user_id:int):
        """Delete generated forecast reports."""
        REPORT_DIR=Path(f"data/users/{user_id}/forecast_reports")
        if REPORT_DIR.exists():
           self._clear_directory(REPORT_DIR)

    def _clear_vector_store(self,user_id:int):
        """Delete FAISS index and associated metadata."""

        vector_dir = Path(f"data/users/{user_id}/vectorstore")

        if vector_dir.exists():
            self._clear_directory(vector_dir)

    def _clear_directory(self, directory: Path):
        """
        Delete all files and subdirectories inside a directory,
        while keeping the directory itself.
        """

        if not directory.exists():
            return

        for item in directory.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                logger.info("Removing file: %s", item)
                item.unlink()


    def _clear_knowledge_documents(self,user_id:int):
        """
        Delete uploaded knowledge documents.

        Adjust the directory if your knowledge upload service
        uses a different storage location.
        """

        docs_dir = Path(f"data/users/{user_id}/uploads")

        if docs_dir.exists():
            self._clear_directory(docs_dir)