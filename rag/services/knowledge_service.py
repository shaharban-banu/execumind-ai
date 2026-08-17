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


    def list_documents(self, user_id: int):
        """
        List uploaded knowledge documents for a user.
        """
        upload_dir = self._get_upload_dir(user_id)

        logger.info(
            "Listing uploaded knowledge documents for user %s.",
            user_id,
        )

        documents = []

        for file in upload_dir.iterdir():
            if file.is_file():
                documents.append({
                    "name": file.name,
                    "size": round(file.stat().st_size / 1024 / 1024, 2),
                    "uploaded_at": file.stat().st_mtime,
                })

        logger.info(
            "Found %d uploaded documents.",
            len(documents),
        )

        return documents

    def _get_upload_dir(self, user_id: int) -> Path:
        """
        Return the knowledge document directory
        for a specific user.
        """
        upload_dir = Path(f"data/users/{user_id}/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        return upload_dir