import json
from utils.logger import logger
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

from rag.reviews.scoring import (reciprocal_rank_fusion)

CHUNKS_PATH=Path("data/processed")/"doc_chunks.json"
INDEX_PATH=Path("data/indexes")/"business_index.faiss"
BM25_PATH=Path("data/indexes")/"docs_bm25_index.pkl"
EMBEDDING_MODEL=("sentence-transformers/"
                 "paraphrase-multilingual-MiniLM-L12-v2")

class HybridBusinessRetriever:
    def __init__(self):
        self.model=SentenceTransformer(EMBEDDING_MODEL)
        self.index=None
        self.bm25=None
        self.chunks=None
        self.load_resources()

    def load_resources(self):
        try:
            logger.info("Loading resources for hybrid retrieval...")
            with open(CHUNKS_PATH,encoding='utf-8')as f:
                self.chunks=json.load(f)
            self.index=faiss.read_index(str(INDEX_PATH))
            with open(BM25_PATH,"rb")as f:
                self.bm25=pickle.load(f)
        except Exception:
            logger.info("resource loading failed")

    def retrieve_faiss(self,query,top_k:int=20):
        embedding=self.model.encode([query],convert_to_numpy=True)
        distances,indices=self.index.search(embedding.astype(np.float32),top_k)
        return indices[0].tolist()
    
    def retrieve_bm25(self,query,top_k:int =20):
        tokens=query.lower().split()
        scores=self.bm25.get_scores(tokens)
        ranked=sorted(enumerate(scores),key=lambda x:x[1],reverse=True)
        return [doc_id for doc_id,_ in ranked[:top_k]]
    
    def retrieve(self,query,top_k:int=20):
        try:
            faiss_result=self.retrieve_faiss(query)
            bm25_result=self.retrieve_bm25(query)

            print("\nFAISS IDS")
            print(faiss_result[:10])

            print("\nBM25 IDS")
            print(bm25_result[:10])


            fused=reciprocal_rank_fusion([faiss_result,bm25_result])


            print("\nFUSED")
            print(fused[:10])
            
            results=[]
            for doc_id,score in fused[:top_k]:
                chunk=self.chunks[doc_id]
                results.append({
                    "score":score,
                    "chunk_id":chunk["chunk_id"],
                    "source":chunk["source"],
                    "page":chunk["page"],
                    "text":chunk["text"]
                })
            logger.info("Retrieved %s business documents",len(results))
            return results
        except Exception:
            logger.exception("Hybrid retrieval failed")
            raise
    
retriever=None
def search_business_docs_hybrid(query,top_k:int=3):
    """
    Search reviews using Hybrid Retrieval.
    """
    global retriever
    try:
        if retriever is None:
            retriever=HybridBusinessRetriever()
        return retriever.retrieve(query=query,top_k=top_k)
    except Exception:
        logger.exception("Business hybrid search failed...")
        raise

if __name__ == "__main__":

    query = (
        "How can companies improve "
        "customer loyalty?")

    results = (
        search_business_docs_hybrid(query))

    print("\nRESULTS")
    print("=" * 80)

    for result in results:
        print(
            f"\nSource: "
            f"{result['source']}")

        print(
            f"Page: "
            f"{result['page']}")

        print(result["text"][:500])
