"""
Review Embedding Module.

Creates vector embeddings from customer review chunks
and stores them for FAISS indexing.
"""

import json
from utils.logger import logger
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

CHUNK_PATH=(Path("rag/reviews/chunks")/"review_chunks.json")
EMBEDDDING_DIR=Path("rag/reviews/embeddings")
EMBEDDING_PATH=(EMBEDDDING_DIR/"review_embeddings.npy")

MODEL_NAME=("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def load_chunks():
    """
    Load review chunks from JSON file.
    """
    try:
        with open(CHUNK_PATH,"r",encoding="utf-8")as f:
            chunks=json.load(f)
        logger.info("loaded %s review chunks",len(chunks))
        return chunks
    except Exception:
        logger.exception("Failed to load review chunks")
        raise

def create_embeddings(texts):
    """
    Generate embeddings for review texts.
    """
    try:
        logger.info("loading embedding model : %s",MODEL_NAME)
        
        model=SentenceTransformer(MODEL_NAME)
        embeddings=model.encode(texts,batch_size=64,show_progress_bar=True,convert_to_numpy=True)
        
        logger.info("generated embeddings :%s ",embeddings.shape)

        return embeddings
    except Exception:
        logger.exception("embedding generation failed")
        raise

def save_embeddings(embeddings):
    """save embeddings to disk."""
    try:
        EMBEDDDING_DIR.mkdir(parents=True,exist_ok=True)
        np.save(EMBEDDING_PATH,embeddings)

        logger.info("Embeddings saved to %s ",EMBEDDING_PATH)
    except Exception:
        logger.exception("Failed to saveembeddings")
        raise

def main():
    """
    Execute embedding pipeline.
    """
    chunks=load_chunks()
    texts=[chunk["text"] for chunk in chunks]
    embeddings=create_embeddings(texts)
    save_embeddings(embeddings)

    logger.info("Review embedding pipeline completed")

if __name__=="__main__":
    main()
