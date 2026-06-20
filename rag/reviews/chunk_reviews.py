"""
Generate review chunks
for the review RAG pipeline.
"""
import json
from pathlib import Path
import pandas as pd

from repositories.review_repository import get_reviews
from utils.logger import logger



def load_data():
    logger.info("Starting review chunking")

    tables=get_reviews()

    print("tables Retrieved")
    return tables

def build_review_metadata(tables):
    """
    Build enriched review dataframe.
    """

    reviews = tables["reviews"]
    orders = tables["orders"]
    customers = tables["customers"]
    order_items = tables["order_items"]
    products = tables["products"]
    sellers = tables["sellers"]

    logger.info("Building review metadata...")

    df=reviews.merge(orders[["order_id","customer_id","order_status","order_purchase_timestamp"]],on="order_id",how="left")
    df=df.merge(customers[["customer_id","customer_state"]],on="customer_id",how="left")
    order_items_small=(order_items[["order_id","product_id","seller_id"]].drop_duplicates("order_id"))
    df=df.merge(order_items_small,on="order_id",how="left")
    df=df.merge(products[["product_id","product_category_name_english"]],on="product_id",how="left")
    df=df.merge(sellers[['seller_id','seller_state']],on='seller_id',how='left')

    logger.info("Metadata dataframe created  : %s rows",len(df))
    return df

def create_review_chunks(df):
    
    chunks=[]

    for _,row in df.iterrows():
     
        review_text=(row.get("review_comment_message"))

        if pd.isna(review_text):
            continue

        review_text = str(review_text).strip()

        if not review_text:
            continue
     
        category=row.get("product_category_name_english","unknown")
        if pd.isna(category):
            category = "unknown"

        customer_state=row.get("customer_state","unknown")
        if pd.isna(customer_state):
            customer_state="unknown"
        
        seller_state=row.get("seller_state","unknown")
        if pd.isna(seller_state):
            seller_state="unknown"

        embedding_text=(f"Category :{category}. "
                        f"Review Score : {row['review_score']}. "
                        f"Customer State : {customer_state}. "
                        f"Text : {review_text}")

        chunk={"chunk_id": len(chunks),
                "source": "reviews",
                "review_id": row["review_id"],
                "order_id": row["order_id"],
                "review_score": int(row["review_score"]),
                "customer_state": customer_state,
                "seller_state": seller_state,
                "product_id": (row["product_id"] if pd.notna(row["product_id"]) else None),
                "seller_id": (row["seller_id"] if pd.notna(row["seller_id"]) else None),
                "product_category": category,
                "order_status": row.get("order_status"),
                "purchase_date": str(row.get("order_purchase_timestamp")),
                "language": "pt",
                "text": review_text,
                "embedding_text": embedding_text}
        chunks.append(chunk)
    logger.info("created %s chunks",len(chunks))
    return chunks
        
def save_chunks(chunks,output_path):
    Path(output_path).parent.mkdir(parents=True,exist_ok=True)
    with open(output_path,"w",encoding="utf-8")as f:
        json.dump(chunks,f,ensure_ascii=False,indent=4)

def main():
    tables=load_data()
    metadata_df=build_review_metadata(tables)
    chunks=create_review_chunks(metadata_df)
    save_chunks(chunks,"data/processed/review_chunks.json")

if __name__=="__main__":
    main()
