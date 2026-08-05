from pathlib import Path
from rag.config.rag_config import load_rag_config

def get_platform_status():

    dataset_ready = (
        Path("data/dataset").exists()
        and any(Path("data/dataset").iterdir())
    )

    forecast_ready = all([
        Path("data/models/revenue.pkl").exists(),
        Path("data/models/orders.pkl").exists(),
        Path("data/models/customers.pkl").exists(),
        Path("data/models/aov.pkl").exists(),
    ])

    rag_config = load_rag_config()

    rag_ready = (
        rag_config.index_path.exists()
        and rag_config.metadata_path.exists()
    )

    platform_ready = (
        dataset_ready
        and forecast_ready
        and rag_ready
    )

    return {
        "dataset_ready": dataset_ready,
        "forecast_ready": forecast_ready,
        "rag_ready": rag_ready,
        "platform_ready": platform_ready,
    }