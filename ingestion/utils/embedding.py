"""
embedding.py

Provides semantic similarity utilities using SentenceTransformer.
"""
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


class EmbeddingSimilarity:
    """
    Computes semantic similarity using SentenceTransformer.

    The model is loaded only once and embeddings are cached
    for improved performance.
    """

    _model = None
    _embedding_cache: dict[str, object] = {}

    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    @classmethod
    def _get_model(cls) -> SentenceTransformer:
        """
        Load the embedding model once.
        """
        if cls._model is None:
            cls._model = SentenceTransformer(cls.MODEL_NAME)

        return cls._model

    @classmethod
    def _encode(cls, text: str):
        """
        Encode text into an embedding.

        Uses caching to avoid recomputation.
        """
        text = text.lower().strip()

        if text not in cls._embedding_cache:

            model = cls._get_model()

            cls._embedding_cache[text] = model.encode(text,convert_to_tensor=True,)

        return cls._embedding_cache[text]

    @classmethod
    def similarity(cls,text1: str,text2: str,) :
        """
        Compute semantic similarity between two strings.

        Returns:
            Similarity score between 0 and 1.
        """

        emb1 = cls._encode(text1)
        emb2 = cls._encode(text2)

        return float(cos_sim(emb1, emb2).item())

    @classmethod
    def best_match(cls,query: str,candidates: list[str],) :
        """
        Find the semantically closest candidate.

        Returns:
            (best_candidate, similarity_score)
        """

        if not candidates:
            return None, 0.0

        query_embedding = cls._encode(query)

        best_candidate = None
        best_score = -1.0

        for candidate in candidates:

            candidate_embedding = cls._encode(candidate)

            score = float(cos_sim(query_embedding,candidate_embedding,).item())

            if score > best_score:
                best_score = score
                best_candidate = candidate

        return best_candidate, best_score