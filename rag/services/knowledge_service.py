"""
Knowledge service.

Provides operations for managing uploaded
knowledge documents.
"""
from pathlib import Path
from utils.logger import logger

class KnowledgeService:

    """
    Service for managing uploaded knowledge documents.
    """

    UPLOAD_DIR = Path("data/uploads")

    def list_documents(self):

        """
        List uploaded knowledge documents.

        Returns:
            List of dictionaries containing document
            metadata including name, size, and upload time.

        Raises:
            RuntimeError:
                If the upload directory cannot be accessed.
        """
        logger.info("Listing uploaded knowledge documents.")

        try:
            self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

            documents = []

            for file in self.UPLOAD_DIR.iterdir():

                if file.is_file():

                    documents.append({
                        "name": file.name,
                        "size": round(file.stat().st_size / 1024 / 1024, 2),
                        "uploaded_at": file.stat().st_mtime
                    })
            logger.info(
                "Found %d uploaded documents.",
                len(documents),
            )

            return documents
        except OSError as exc:
            logger.exception(
                "Failed to access upload directory '%s'.",
                self.UPLOAD_DIR,
            )
            raise RuntimeError(
                "Unable to list uploaded documents."
            ) from exc