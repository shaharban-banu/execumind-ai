"""Document retrieval module"""
import json
from utils.logger import logger
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

CHUNK_PATH=Path("rag/docs/chunks")/"doc_chunks.json"
INDEX_PATH=Path("rag/docs/index")/"business_index.faiss"
MODEL_NAME=("sentence-transformers/"
            "paraphrase-multilingual-MiniLM-L12-v2")

# Load Resources
#-----------------------------------------------------------
def load_chunks():
    """
    Load document chunks.

    Returns:
        list[dict]:
            document chunk data.
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
            Business index.
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
def search_business_docs(query,top_k:int=5):
    """
    Search business knowledge documents using semantic similarity.

    Args:
        query:
            User query.

        top_k:
            Number of results to retrieve.

    Returns:
        list[dict]:
            Retrieved document chunks.
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
        seen_chunk_ids = set()
        for rank,idx in enumerate(indices[0]):
            chunk = chunks[idx]

            chunk_id = chunk["chunk_id"]

            if chunk_id in seen_chunk_ids:
                continue

            seen_chunk_ids.add(
                chunk_id
            )
            result.append({
                'distance':float(distance[0][rank]),
                'chunk_id':chunks[idx]["chunk_id"],
                'source':chunks[idx]['source'],
                'page':chunks[idx]['page'],
                'text':chunks[idx]['text']
            })

        logger.info("Retrieved %s business document chunks",len(result))
        return result
    except Exception:
        logger.exception("Business document Retrieval Failed")
        raise
# Test
#--------------------------------------------------
if __name__=="__main__":
    query="mobile commerce trends in Brazil"
    results=search_business_docs(query=query,top_k=5)

    print("\n"+"="*80)
    print(f"query : {query}")
    for i,result in enumerate(results,start=1):
        print(f"\nResult {i}")
        print(f"Distance : {result['distance']:.4f}")
        print(f"Source :{result['source']}")
        print(f"Page :{result['page']}")
        print(f"Chunk_id :{result['chunk_id']}")
        print(f"Text :{result['text'][:300]}")
        print("\n"+"="*80)

