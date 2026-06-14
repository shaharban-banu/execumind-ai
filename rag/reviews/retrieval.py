"""Review retrieval module"""
import json
from utils.logger import logger
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

CHUNK_PATH=Path("rag/reviews/chunks")/"review_chunks.json"
INDEX_PATH=Path("rag/reviews/index")/"review_index.faiss"
MODEL_NAME=("sentence-transformers/"
            "paraphrase-multilingual-MiniLM-L12-v2")

# Load Resources
#-----------------------------------------------------------
def load_chunks():
    """
    Load review chunks.

    Returns:
        list[dict]:
            Review chunk data.
    """
    try:
        with open(CHUNK_PATH,'r',encoding='utf-8')as f:
            chunks=json.load(f)
        logger.info("loaded %s chunks",len(chunks))
        return chunks
    except Exception:
        logger.exception("Failed to load chunks")
        raise

def load_index():
    """
    Load FAISS index.

    Returns:
        faiss.Index:
            Review index.
    """
    try:
        index=faiss.read_index(str(INDEX_PATH))
        logger.info("loaded FAISS index")
        return index
    except Exception:
        logger.exception("Failed to load index")
        raise

def load_model():
    """
    Load embedding model.

    Returns:
        SentenceTransformer:
            Embedding model.
    """
    try:
        model=SentenceTransformer(MODEL_NAME)
        logger.info("Loaded Embedding Model")
        return model
    except Exception:
        logger.exception("Failed to load embedding model")
        raise

# Retrieval
#-----------------------------------------------------------
def search_reviews(query,top_k:int=5):
    """
    Search similar customer reviews.

    Args:
        query:
            User query.

        top_k:
            Number of reviews to retrieve.

    Returns:
        list[dict]:
            Retrieved reviews.
    """
    try:
        chunks=load_chunks()
        index=load_index()
        model=load_model()

        query_embedding=model.encode([query],convert_to_numpy=True)
        distance,indices=index.search(
            query_embedding.astype('float32'),
            top_k
            )
        result=[]
        for idx in indices[0]:
            result.append(chunks[idx])

        logger.info("Retrieved %s reviews",len(result))
        return result
    except Exception:
        logger.exception("Review Retrieval Failed")
        raise
# Test
#--------------------------------------------------
if __name__=="__main__":
    query="poor packaging"
    results=search_reviews(query=query,top_k=5)

    print("\n"+"="*80)
    print(f"query : {query}")
    for i,result in enumerate(results,start=1):
        print(f"\nResult {i}")
        print(f"score :{result['review_score']}")
        print(f"text : {result['text']}")

