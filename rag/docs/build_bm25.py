"""
Build BM25 index for business document chunks.
This module:
1. Loads document chunks.
2. Tokenizes document texts.
3. Builds BM25 index.
"""
from pathlib  import Path
import json
import pickle
from utils.logger import logger
from rank_bm25 import BM25Okapi

CHUNK_PATH=Path("data/processed")/"doc_chunks.json"
INDEX_DIR=Path("data/indexes")
INDEX_PATH=INDEX_DIR/"docs_bm25_index.pkl"

def load_chunks():
    """
    Load document chunks.
    """
    logger.info("Loading document chunks..")
    with open(CHUNK_PATH,"r",encoding="utf-8") as f:
        chunks=json.load(f)
    
    logger.info("%s chunks loaded",len(chunks))
    return chunks

def extract_texts(chunks):
    """
    Extract texts used for BM25 indexing.
    """
    texts=[]
    for chunk in chunks:
        text=chunk["text"]
        texts.append(text)
    return texts

def tokenize(texts):
    """tokenize text for BM25"""
    logger.info("Tokenizing %s texts",len(texts))

    return [text.lower().split() for text in texts]

def build_index(tokenised_texts):
    """build BM25 index"""
    logger.info("building BM25 index...")

    bm25=BM25Okapi(tokenised_texts)

    logger.info("BM25 index created.")
    return bm25

def save_index(bm25):
    INDEX_DIR.mkdir(parents=True,exist_ok=True)
    with open(INDEX_PATH,"wb")as f:
        pickle.dump(bm25,f)
    logger.info("BM25 index savedto %s",INDEX_PATH)

def main():
    try:
        logger.info("-"*50)
        logger.info("Building Review BM25 index")
        logger.info("-"*50)
        chunks=load_chunks()
        texts=extract_texts(chunks)
        tokenised=tokenize(texts)
        bm25=build_index(tokenised)
        save_index(bm25)

        logger.info("BM25 build completed....")
    except Exception:
        logger.exception("Failed to build BM25 index")
        raise

if __name__=="__main__":
    main()