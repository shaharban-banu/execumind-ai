"""
Business Document Extraction Module.

Extracts text from PDF documents and stores
page-level content with metadata.
"""
import json
from utils.logger import logger
from pathlib import Path
from pypdf import PdfReader

RAW_DOCS_DIR=Path("rag/docs/raw_docs")
OUTPUT_DIR=Path("rag/docs/extracted")
OUTPUT_FILE=(OUTPUT_DIR/"documents.json")

def extract_pdf(pdf_path:Path):
    """
    Extract page-level text from PDF.

    Args:
        pdf_path:
            Path to PDF.

    Returns:
        List of page documents.
    """
    try:
        reader=PdfReader(str(pdf_path))
        pages=[]
        for page_num,page in enumerate(reader.pages,start=1):
            text=(page.extract_text() or "")
            pages.append({
                "source":pdf_path.stem,
                "page":page_num,
                "text":text
            })
        logger.info("extracted %s pages from %s",len(pages),pdf_path.name)
        return pages
    except Exception:
        logger.exception("Failed to process %s",pdf_path)
        raise

def main():
    OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
    all_pages=[]
    pdf_files=list(RAW_DOCS_DIR.glob("*.pdf"))

    logger.info("Found %s PDF",len(pdf_files))

    for pdf in pdf_files:
        pages=extract_pdf(pdf)
        all_pages.extend(pages)
    
    with open(OUTPUT_FILE,"w",encoding="utf-8")as f:
        json.dump(all_pages,f,ensure_ascii=False,indent=4)

    logger.info("Saved %s pages",len(all_pages))

if __name__=="__main__":
    main()
