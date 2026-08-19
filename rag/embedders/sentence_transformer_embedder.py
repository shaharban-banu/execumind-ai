"""
SentenceTransformer embedding model.
"""
from utils.logger import logger
from sentence_transformers import SentenceTransformer
from rag.embedders.base_embedder import BaseEmbedder

class SentenceTransformerEmbedder(BaseEmbedder):
    """
    SentenceTransformer embedding model.
    """
    _cached_models={}
    def __init__(self,model_name:str,batch_size:int=64,):
        """
        Initialize the SentenceTransformer embedding model.

        Args:
            model_name: Name or path of the embedding model.
            batch_size: Number of texts to encode per batch.
        """

        if model_name not in self._cached_models:
            self._cached_models[model_name] = SentenceTransformer(model_name)

        self.model = self._cached_models[model_name]
        self.batch_size = batch_size
        logger.info("Loaded embedding model %s",model_name)

    def embed(self, texts):
        """
        Generate embeddings for the given texts.

        Args:
            texts: Collection of text strings to encode.

        Returns:
            List of embedding vectors.
        """

        embeddings = self.model.encode(texts,
                                     batch_size=self.batch_size,
                                     show_progress_bar=True,
                                     convert_to_numpy=True,
                                     normalize_embeddings=True)
        return embeddings.tolist()

