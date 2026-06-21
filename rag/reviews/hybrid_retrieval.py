import json
import logging
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

from rag.reviews.scoring import (reciprocal_rank_fusion)

CHUNKS_PATH=Path("data/processed")/"review_chunks.json"
INDEX_PATH=Path("data/indexes")/"review_index.faiss"
BM25_PATH=Path("data/indexes")/"reviews_bm25_index.pkl"
EMBEDDING_MODEL=("sentence-transformers/"
                 "paraphrase-multilingual-MiniLM-L12-v2")

class HybridReviewRetriever:
    def __init__(self):
        self.model=SentenceTransformer(EMBEDDING_MODEL)
        self.index=None
        self.bm25=None
        self.chunks=None
        self.load_resources()

    def load_resources(self):
        with open(CHUNKS_PATH,encoding='utf-8')as f:
            self.chunks=json.load(f)
        self.index=faiss.read_index(str(INDEX_PATH))
        with open(BM25_PATH,"rb")as f:
            self.bm25=pickle.load(f)

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
                "source":"review",
                "review_id":chunk["review_id"],
                "text":chunk["text"],
                "metadata":chunk
            })

        return results
    
retriever=None
def search_reviews_hybrid(query,top_k:int=3):
    """
    Search reviews using Hybrid Retrieval.
    """
    global retriever
    if retriever is None:
        retriever=HybridReviewRetriever()
    return retriever.retrieve(query=query,top_k=top_k)
