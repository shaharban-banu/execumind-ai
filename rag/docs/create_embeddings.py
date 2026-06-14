import json
from utils.logger import logger
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

CHUNK_PATH=Path("rag/docs/chunks")/"doc_chunks.json"
EMBEDDING_DIR=Path("rag/docs/embeddings")
EMBEDDING_PATH=(EMBEDDING_DIR/"doc_embeddings.npy")

MODEL_NAME=("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def load_chunks():
    """
    Load document chunks from JSON file"""
    try:
        with open(CHUNK_PATH,'r',encoding='utf-8')as f:
            chunks=json.load(f)

        logger.info("Loaded %s document chunks",len(chunks))
        return chunks
    except Exception:
        logger.exception("Failed to load document chunks")
        raise
def create_embeddings(texts):
    """
    Generate embeddings for document texts.
    """
    try:
        logger.info("Loading embedding model : %s",MODEL_NAME)

        model=SentenceTransformer(MODEL_NAME)
        embeddings=model.encode(texts,batch_size=64,show_progress_bar=True,convert_to_numpy=True)

        logger.info("generated embeddings : %s",embeddings.shape)

        return embeddings
    except Exception:
        logger.exception("embedding generation failed")
        raise

def save_embedding(embeddings):
    """save embeddings to disk."""
    try:
        EMBEDDING_DIR.mkdir(parents=True,exist_ok=True)
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
    texts=[chunk['text'] for chunk in chunks]
    embeddings=create_embeddings(texts)
    save_embedding(embeddings)

    logger.info("Document embedding pipeline completed")

if __name__=="__main__":
    main()
