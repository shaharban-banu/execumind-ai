"""
Business Document Chunking Module.

Splits extracted PDF pages into smaller chunks
for embedding generation and semantic retrieval.
"""
import json
from utils.logger import logger
from pathlib import Path
from langchain_text_splitters import (RecursiveCharacterTextSplitter)

EXTRACTED_PATH=Path("rag/docs/extracted")/"documents.json"
CHUNK_DIR=Path("rag/docs/chunks")
CHUNK_PATH=(CHUNK_DIR/"doc_chunks.json")

CHUNK_SIZE=700
CHUNK_OVERLAP=150

def load_documents():
    """
    Load extracted PDF pages.

    Returns:
        list[dict]:
            Extracted page documents.
    """
    try:
        with open(EXTRACTED_PATH,'r',encoding='utf-8')as f:
            documents=json.load(f)

        logger.info("Loaded %s pages",len(documents))

        return documents
    except Exception:
        logger.exception("Failed to load documents")
        raise

def chunk_documents(documents):
    """
    Split page documents into chunks.

    Args:
        documents:
            Extracted page documents.

    Returns:
        list[dict]:
            Chunked documents.
    """
    try:
        splitter=(RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,
                                                 chunk_overlap=CHUNK_OVERLAP,
                                                 length_function=len))
        chunks=[]
        chunk_id=1
        for document in documents:
            source=document["source"]
            page=document["page"]
            text=document["text"]

            if not text.strip():
                continue
            split_texts=(splitter.split_text(text))
            for chunk_text in split_texts:
                chunks.append(
                    {
                        'chunk_id':chunk_id,
                        'source':source,
                        'page':page,
                        'text':chunk_text
                    }
                )
            chunk_id+=1
        logger.info("created %s chunks",len(chunks))
            
        return chunks
    except Exception:
        logger.exception("chunking failed")
        raise

def save_chunks(chunks):
    """
    Save chunks to JSON.

    Args:
        chunks:
            Chunked documents.
    """
    try:
        CHUNK_DIR.mkdir(parents=True,exist_ok=True)
        with open(CHUNK_PATH,'w',encoding='utf-8')as f:
            json.dump(chunks,f,ensure_ascii=False,indent=4)
        logger.info("Saved chunks to %s",CHUNK_PATH)
    except Exception:
        logger.exception("Failed to save chunks")
        raise

def main():
    """
    Execute document chunking pipeline.
    """
    documents=load_documents()
    chunks=chunk_documents(documents)
    save_chunks(chunks)

    logger.info("Documents chunking completed")

if __name__=="__main__":
    main()

        
