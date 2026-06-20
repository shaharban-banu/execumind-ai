"""
FAISS Index Builder.

Builds a FAISS vector index from review embeddings.
"""

from pathlib import Path

import faiss
import numpy as np
from utils.logger import logger
# --------------------------------------------------
# Paths
# --------------------------------------------------

EMBEDDING_PATH = (
    Path("data/embeddings")
    / "review_embeddings.npy"
)

INDEX_DIR = Path(
    "data/indexes"
)

INDEX_PATH = (
    INDEX_DIR
    / "review_index.faiss"
)


def load_embeddings() -> np.ndarray:
    """
    Load review embeddings.
    """

    try:

        embeddings = np.load(EMBEDDING_PATH)

        logger.info(
            "Loaded embeddings: %s",embeddings.shape)

        return embeddings

    except Exception:

        logger.exception("Failed to load embeddings")
        raise


def build_index(
    embeddings: np.ndarray
) -> faiss.Index:
    """
    Create FAISS index.
    """

    try:

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(
            dimension
        )

        index.add(
            embeddings.astype(
                "float32"
            )
        )

        logger.info(
            "Indexed %s vectors",
            index.ntotal
        )

        return index

    except Exception:

        logger.exception(
            "Failed to build index"
        )
        raise


def save_index(
    index: faiss.Index
) -> None:
    """
    Save FAISS index.

    """

    try:

        INDEX_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            index,
            str(INDEX_PATH)
        )

        logger.info(
            "Index saved: %s",
            INDEX_PATH
        )

    except Exception:

        logger.exception(
            "Failed to save index"
        )
        raise


def main() -> None:

    embeddings = load_embeddings()

    index = build_index(
        embeddings
    )

    save_index(
        index
    )

    logger.info(
        "FAISS index creation completed"
    )


if __name__ == "__main__":
    main()