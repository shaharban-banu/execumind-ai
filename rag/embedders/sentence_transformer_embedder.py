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
    def __init__(self,model_name:str,batch_size:int=64,):
        """initialize embedding model"""

        self.model=SentenceTransformer(model_name)
        self.batch_size=batch_size
        logger.info("Loaded mbedding model %s",model_name)

    def embed(self, texts):
        """generate embeddings"""

        embeddings=self.model.encode(texts,
                                     batch_size=self.batch_size,
                                     show_progress_bar=True,
                                     convert_to_numpy=True,
                                     normalize_embeddings=True)
        return embeddings.tolist()

