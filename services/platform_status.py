from pathlib import Path
from database.database import SessionLocal

from database.models import Dataset,DatasetVersion

def get_platform_status(user_id:int):

    model_dir = Path(f"data/users/{user_id}/models")
    forecast_ready = all([
        (model_dir / "revenue.pkl").exists(),
        (model_dir / "orders.pkl").exists(),
        (model_dir / "customers.pkl").exists(),
        (model_dir / "aov.pkl").exists(),
    ])

    vector_dir = Path(f"data/users/{user_id}/vectorstore")

    rag_ready = (
        (vector_dir / "faiss.index").exists()
        and (vector_dir / "metadata.pkl").exists()
    )

    db = SessionLocal()

    dataset_ready = (
        db.query(DatasetVersion)
        .join(Dataset)
        .filter(
            Dataset.user_id == user_id,
            DatasetVersion.is_active == True,
        )
        .first()
        is not None
    )

    db.close()

    return {
        "dataset_ready": dataset_ready,
        "forecast_ready": forecast_ready,
        "rag_ready": rag_ready,
        "platform_ready": (
            dataset_ready and forecast_ready and rag_ready
        ),
    }