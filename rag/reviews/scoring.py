"""Reciprocal rank fusion scoring"""

from collections import defaultdict

def reciprocal_rank_fusion(rankings,k:int=60):
    """combine rankings using RRF"""

    scores=defaultdict(float)

    for ranking in rankings:
        for rank,doc_id in enumerate(ranking):
            scores[doc_id]+=(1/(k+rank+1))
    return sorted(scores.items(),key=lambda x:x[1],reverse=True)