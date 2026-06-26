"""cross Encoder Reranker"""

from sentence_transformers import CrossEncoder
from utils.logger import logger

MODEL_NAME= "BAAI/bge-reranker-v2-m3"

class CrossEncoderReranker:
    def __init__(self):
        try:
            logger.info("Loading cross encoder..")
            self.model=CrossEncoder(MODEL_NAME)
            logger.info("Cross encoder loaded...")
        except Exception:
            logger.exception("Failed loading reranker")
            raise
    def rerank(self,query,documents,top_k):
        """rerank retrieved documents"""
        try:
            if not documents:
                return []
            pairs=[(query,doc['text']) for doc in documents]
            scores=(self.model.predict(pairs))
            print("SCORES   :",scores)
            for doc,score in zip(documents,scores):
                doc['rerank_score']=float(score)
            ranked=sorted(documents,key=lambda x:x['rerank_score'],reverse=True)

            return ranked[:top_k]
        except Exception:
            logger.info("Reranking Failed...")
            raise
        