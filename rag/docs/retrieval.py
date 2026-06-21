"""Document retrieval module"""
import json,re
from utils.logger import logger
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

CHUNK_PATH=Path("data/processed")/"doc_chunks.json"
INDEX_PATH=Path("data/indexes")/"business_index.faiss"
EMBEDDING_PATH=Path("data/embeddings")/"doc_embeddings.npy"
MODEL_NAME=("sentence-transformers/"
            "paraphrase-multilingual-MiniLM-L12-v2")

#source groupings for filtered retrieval
SOURCE_GROUPS = {
    "olist_docs": {
        "olist_company_overview",
        "olist_business_strategy",
        "olist_executive_playbook",
    },
    "research": {
        "consumer_behavior",
        "ecommerce_analysis",
    },
}

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

def load_embeddings():
    """
    Load raw document embeddings (needed for building
    filtered sub-indexes when source_filter is used).
 
    Returns:
        np.ndarray:
            Document embeddings.
    """
    try:
        embeddings=np.load(EMBEDDING_PATH)
        logger.info("loaded embeddings : %s",embeddings.shape)
        return embeddings
    except Exception:
        logger.exception("Failed to load embeddings")
        raise

_chunks=None
_index=None
_model=None
_embeddings=None

def _get_resources():
    global _chunks,_index,_model,_embeddings
    if _index is None:
        _index=load_index()
    if _chunks is None:
        _chunks=load_chunks()
    if _embeddings is None:
        _embeddings=load_embeddings()
    if _model is None:
        _model=load_model()
    return _chunks,_index,_model,_embeddings

# Retrieval
#-----------------------------------------------------------
def search_business_docs(query,top_k:int=5,source_filter:str="all"):
    """
    Search business knowledge documents using semantic similarity.

    Args:
        query:
            User query.

        top_k:
            Number of results to retrieve.

    source_filter:
            "all"        — search all documents (default)
            "olist_docs" — only Olist strategy documents
                           (company_overview, business_strategy,
                           executive_playbook)
            "research"   — only research papers
                           (consumer_behavior, ecommerce_analysis)
            Any exact source name — e.g. "olist_executive_playbook"

    Returns:
        list[dict]:
            Retrieved document chunks.
    """
    try:
        chunks,index,model,embeddings=_get_resources()

        # Resolve allowed sources for this filter
        if source_filter=="all":
            allowed_sources=None
        elif source_filter in SOURCE_GROUPS:
            allowed_sources=SOURCE_GROUPS[source_filter]
        else:
            allowed_sources={source_filter}
 
        query_embedding=model.encode([query],convert_to_numpy=True)

        if allowed_sources is None:
            #no filter -search full
            search_chunks=chunks

            distance,indices=index.search(
                query_embedding.astype('float32'),
                top_k
                )
        else:
            # Filtered — build a small sub-index from only the
            # chunks whose source is in allowed_sources
            filtered=[
                (i,c) for i,c in enumerate(chunks)
                if c["source"] in allowed_sources
            ]
 
            if not filtered:
                logger.warning(
                    "No chunks found for source_filter=%s",
                    source_filter
                )
                return []
 
            filtered_indices=[i for i,_ in filtered]
            search_chunks=[c for _,c in filtered]
 
            sub_embeddings=embeddings[filtered_indices].astype('float32')
            dimension=sub_embeddings.shape[1]
            sub_index=faiss.IndexFlatL2(dimension)
            sub_index.add(sub_embeddings)
 
            distance,indices=sub_index.search(
                query_embedding.astype('float32'),
                min(top_k,len(search_chunks))
                )

        result=[]
        seen_chunk_ids = set()
        for rank,idx in enumerate(indices[0]):
            if idx == -1:
                continue
            chunk = search_chunks[idx]

            chunk_id = chunk["chunk_id"]

            if chunk_id in seen_chunk_ids:
                continue

            seen_chunk_ids.add(
                chunk_id
            )
            result.append({
                'distance':float(distance[0][rank]),
                'chunk_id':chunk["chunk_id"],
                'source':chunk['source'],
                'page':chunk['page'],
                'text':chunk['text']
            })

        logger.info("Retrieved %s business document chunks",len(result))
        return result
    except Exception:
        logger.exception("Business document Retrieval Failed")
        raise


def search_olist_strategy(query,top_k:int=3):
    """
    Shortcut: search only Olist internal documents.
 
    Used by Executive Advisor Agent to ground responses
    in Olist-specific strategy and playbook knowledge.
    """
    return search_business_docs(
        query=query,
        top_k=top_k,
        source_filter="olist_docs"
    )
 
 
def search_market_research(query,top_k:int=3):
    """
    Shortcut: search only market research papers.
 
    Used by Customer Intelligence Agent to ground
    responses in consumer behavior and market data.
    """
    return search_business_docs(
        query=query,
        top_k=top_k,
        source_filter="research"
    )
 
 

# Test
#--------------------------------------------------
if __name__=="__main__":
    query="mobile commerce trends in Brazil"
    results=search_business_docs(query=query,top_k=5)

    print("\n"+"="*80)
    print("Test 1 — default (all sources)")
    print("="*80)
    results=search_business_docs(query=query,top_k=5)
    for i,result in enumerate(results,start=1):
        print(f"\nResult {i}")
        print(f"Distance : {result['distance']:.4f}")
        print(f"Source :{result['source']}")
        print(f"Page :{result['page']}")
        print(f"Chunk_id :{result['chunk_id']}")
        print(f"Text :{result['text'][:300]}")
 
    print("\n"+"="*80)
    print("Test 2 — olist_docs only")
    print("="*80)
    results=search_olist_strategy(query="how to respond to declining sales")
    for i,result in enumerate(results,start=1):
        print(f"\nResult {i}")
        print(f"Source :{result['source']}")
        print(f"Text :{result['text'][:200]}")
 
    print("\n"+"="*80)
    print("Test 3 — research only")
    print("="*80)
    results=search_market_research(query="customer loyalty repeat purchases")
    for i,result in enumerate(results,start=1):
        print(f"\nResult {i}")
        print(f"Source :{result['source']}")
        print(f"Text :{result['text'][:200]}")
 

