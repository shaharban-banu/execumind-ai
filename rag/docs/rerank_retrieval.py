"""Business document retrieval with ranking"""

from rag.docs.hybrid_retrieval import (search_business_docs_hybrid)
from rag.reranker.cross_encoder import (CrossEncoderReranker)

reranker = None
def get_reranker():
    global reranker

    if reranker is None:
        reranker=CrossEncoderReranker()
    return reranker


def search_business_docs_rerank(query,top_k:int=3):
    """Hybrid retrieval followed by reranking"""

    candidates=search_business_docs_hybrid(query=query,top_k=20)
    
    reranker = get_reranker()
    reranked=reranker.rerank(query=query,documents=candidates,top_k=top_k)

    return reranked
    
# #test-------
# if __name__ == "__main__":
#     results = search_business_docs_rerank(
#         "What factors influence customer loyalty in Brazilian e-commerce?"
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
#             f"Source: {r['source']}"
#         )
#         print(
#             f"Text: {r['text'][:300]}"
#         )
#         print("-" * 80)