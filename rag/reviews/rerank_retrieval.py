"""review retrieval with reranking"""

from rag.reranker.cross_encoder import (CrossEncoderReranker)
from rag.reviews.hybrid_retrieval import (search_reviews_hybrid)

reranker = None
def get_reranker():
    global reranker

    if reranker is None:
        reranker=CrossEncoderReranker()
    return reranker

def search_reviews_rerank(query,top_k:int=3):
    """Hybrid retrieval followed by reranking"""
    candidates=(search_reviews_hybrid(query=query,top_k=20))
    print("LENGTH OF CANDIDATES   :",len(candidates))
    print("\nHYBRID")
    for doc in candidates:
        print(doc["chunk_id"],doc["text"][:100])
    reranker = get_reranker()
    reranked=reranker.rerank(query=query,documents=candidates,top_k=top_k)
    print("\nRERANKED")
    for doc in reranked:
    
        print(
        doc["chunk_id"],
        doc["rerank_score"])
    return reranked


#test------------

# if __name__ == "__main__":
#     results = search_reviews_rerank(
#         "Why are customers complaining about late deliveries?"
#     )

#     print("\nRERANKED RESULTS")
#     print("=" * 80)

#     for r in results:
#         print(
#             f"Chunk ID: {r['chunk_id']}"
#         )
#         print(
#             f"Score: {r['rerank_score']}"
#         )
#         print(
#             f"Text: {r['text'][:200]}"
#         )
#         print("-" * 80)