from pathlib import Path
from sqlalchemy.orm import Session

from database.models import DatasetVersion, Dataset
from database.database import SessionLocal

def get_active_dataset_path(user_id: int) -> Path:
    db: Session = SessionLocal()

    try:
        version = (
            db.query(DatasetVersion)
            .join(Dataset)
            .filter(
                Dataset.user_id == user_id,
                DatasetVersion.is_active == True,
            )
            .first()
        )

        if version is None:
            raise FileNotFoundError("No active dataset version selected.")

        return Path(
            f"data/users/{user_id}/datasets/"
            f"{version.dataset.name}/v{version.version_number}"
        )

    finally:
        db.close()