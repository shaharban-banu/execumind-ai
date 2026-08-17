from pathlib import Path

def get_user_vectorstore_paths(user_id: int):
    """
    Return the FAISS index and metadata paths
    for a user's vector store.
    """

    base = Path(f"data/users/{user_id}/vectorstore")
    base.mkdir(parents=True, exist_ok=True)

    return (
        base / "faiss.index",
        base / "metadata.pkl",
    )