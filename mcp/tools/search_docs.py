"""
Unified Document Search Tool.

Combines review retrieval and
business document retrieval
into a single interface.
"""
from utils.logger import logger
from rag.reviews.retrieval import (search_reviews,)
from rag.docs.retrieval import(search_business_docs,)
from rag.reviews.hybrid_retrieval import (search_reviews_hybrid,)

def search_docs(query,review_top_k:int=3,business_top_k:int=3,method:str="faiss"):
    """
    Search across all knowledge sources.

    Args:
        query:
            User query.

        review_top_k:
            Number of review chunks.

        business_top_k:
            Number of business chunks.

    Returns:
        dict:
            Combined retrieval results.
    """
    try:
        logger.info("SEARCH METHOD = %s",method)
        print(f"SEARCH METHOD = {method}")
        if method=="hybrid":
            review_results=(search_reviews_hybrid(query=query,top_k=review_top_k))
        else:
            review_results=(search_reviews(query=query,top_k=review_top_k))
        business_results=(search_business_docs(query=query,top_k=business_top_k))

        results={
            'reviews':review_results,
            'business_docs':business_results
        }

        logger.info("Retrieved documents"
                    "for query : %s  using method %s",query,method)
        return results
    except Exception:
        logger.exception("Unified search failed")
        raise

#Test Block
if __name__=="__main__":
    query="How should executives respond to declining sales?"
    results=search_docs(query=query,method="hybrid")

    print("\nReviews")
    print("="*80)

    for review in results["reviews"]:
        print(review['text'][:200])

    print("\nBusiness docs")
    print("="*80)

    for doc in results["business_docs"]:
        print(f"{doc['source']}"
              f"(page {doc['page']})")
        print(doc['text'][:200])