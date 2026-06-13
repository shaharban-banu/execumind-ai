"""
Generate review chunks
for the review RAG pipeline.
"""
import json
from pathlib import Path

from repositories.review_repository import get_reviews
from utils.logger import logger

Path("rag/reviews/chunks").mkdir(parents=True,exist_ok=True)
logger.info("Starting review chunking")

df=get_reviews()

print(f"Reviews Retrieved : {len(df)}")

chunks=[]

for _,row in df.iterrows():
    review_text=str(row['review_comment_message']).strip()

    if review_text and review_text.lower()!='nan':
        chunks.append({
            'review_id':row['review_id'],
            'order_id':row['order_id'],
            'review_score':int(row['review_score']),
            'text':review_text
        }
        )
with open("rag/reviews/chunks/review_chunks.json","w",encoding="utf-8")as f:
    json.dump(chunks,f,ensure_ascii=False,indent=4)

logger.info(f"Created {len(chunks)} chunks")
