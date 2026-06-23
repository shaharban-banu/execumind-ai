"""
Manual Document Cleaner.

Removes known noise pages from the extracted documents.json
before chunking. This is cleaner than post-hoc chunk filtering
because noise is removed at the page level — before RecursiveCharacterTextSplitter
runs — so no chunk ever contains a mix of real content and boilerplate.

Edit PAGES_TO_DROP and TEXT_TO_STRIP below as you inspect your
extracted documents.json and find pages worth removing.

Run order:
    extract_docs.py  →  clean_docs.py  →  chunk_docs.py
"""
import json
from pathlib import Path
from utils.logger import logger

EXTRACTED_PATH = Path("rag/docs/extracted") / "documents.json"
CLEAN_PATH = Path("rag/docs/extracted") / "cleaned_documents.json"


# --------------------------------------------------
# Edit these two sections to configure what gets removed
# --------------------------------------------------

# Entire pages to drop — identified by (source, page_number).
# These pages are 100% boilerplate with no useful content.
PAGES_TO_DROP: set[tuple[str, int]] = {
    # consumer_behavior — title page and citation block
    ("consumer_behavior", 1),
    ("consumer_behavior", 3),
    ("consumer_behavior", 22),
    ("consumer_behavior", 23),
    ("consumer_behavior", 24),

    # ecommerce_analysis — references and closing license
    # Pages 18-19 are entirely references + Open Access text
    ("ecommerce_analysis", 18),
    ("ecommerce_analysis", 19),
}

# Text fragments to strip from individual pages.
# Use this for pages that are MOSTLY real content but have
# a header/footer/watermark appended by the PDF extractor.
# Format: {(source, page): [list of strings to remove]}
TEXT_TO_STRIP: dict[tuple[str, int], list[str]] = {
    # ecommerce_analysis page 1 has real intro content but
    # also has the conference citation footer appended at bottom
    ("ecommerce_analysis", 1): [
        "\n Saikiran Gogineni1,, Yuvaraju Chinnam1,, Kanaka Durga Returi2, Vaka Murali",
        "Mohan3, G Suryanarayana4",
        "1Department of Computer Science and Engineering, Malla Reddy (MR) Deemed to be university,",
        "Hyderabad, India,",
        "2Department of Computer Science and Engineering,  Malla  Reddy  Vishwavidyapeeth  (Deemed  ",
        "to be university), Hyderabad, India. ",
        "3Department of Computer Science and Engineering, Malla Reddy College of Engineering and ",
        "Technology, Hyderabad, India. ",
        "4Department of Computer Science and Engineering, Symbiosis Institute of Technology,",
        "Hyderabad Campus, Symbiosis International (Deemed University), Pune, India.  ",
        "1goginenisaikiran31677@gmail.com, 2chinnamyuvaraj@gmail.com,",
        "3durga1210@gmail.com, 4vakamuralimohan@gmail.com, ",
        "5surya.aits@gmail.com ",
        "© The Author(s) 2025",
        "P. Bagchi et al. (eds.), Proceedings of the International Conference on Intelligent Information Systems Design and\nIndian Knowledge System Applications (ICISDIKSA 2026), Advances in Intelligent Systems Research 203,\nhttps://doi.org/10.2991/978-94-6463-976-6_6",
        "End-to-End Data Analysis of Brazilian E-Commerce Transactions 83",
    ],

    # Add more entries here as you find noise in other pages:
    # ("olist_company_overview", 1): ["Page header text to remove"],
}

# Minimum chars of content worth keeping after stripping.
# Pages below this threshold are dropped even if not in PAGES_TO_DROP.
MIN_PAGE_CONTENT_LENGTH = 50


# --------------------------------------------------
# Cleaner logic — no edits needed below this line
# --------------------------------------------------

def clean_page_text(source: str, page: int, text: str) -> str:
    """
    Strip known noise fragments from a page's text.

    Args:
        source: Document source name.
        page: Page number.
        text: Extracted page text.

    Returns:
        Cleaned text with known fragments removed.
    """
    fragments = TEXT_TO_STRIP.get((source, page), [])
    cleaned = text
    for fragment in fragments:
        cleaned = cleaned.replace(fragment, "")
    return cleaned.strip()


def clean_documents(documents: list[dict]) -> list[dict]:
    """
    Remove known noise pages and strip noise fragments.

    Args:
        documents: Extracted page documents from documents.json.

    Returns:
        Cleaned documents ready for chunking.
    """
    clean = []
    dropped_pages = []
    stripped_pages = []

    for doc in documents:
        source = doc["source"]
        page = doc["page"]
        text = doc["text"]

        # Drop entire page if in the drop list
        if (source, page) in PAGES_TO_DROP:
            dropped_pages.append((source, page))
            continue

        # Strip known noise fragments from the page text
        cleaned_text = clean_page_text(source, page, text)

        # Drop if remaining content is too short to be useful
        if len(cleaned_text) < MIN_PAGE_CONTENT_LENGTH:
            dropped_pages.append((source, page))
            continue

        # Track pages where text was modified
        if cleaned_text != text.strip():
            stripped_pages.append((source, page))

        clean.append({
            "source": source,
            "page": page,
            "text": cleaned_text
        })

    logger.info(
        "Document cleaner: kept %s pages, dropped %s pages",
        len(clean), len(dropped_pages)
    )
    if dropped_pages:
        logger.info("Dropped pages: %s", dropped_pages)
    if stripped_pages:
        logger.info("Stripped noise fragments from pages: %s", stripped_pages)

    return clean


def main() -> None:
    """
    Load extracted documents, clean them, save to documents_clean.json.
    """
    logger.info("Loading extracted documents")
    with open(EXTRACTED_PATH, "r", encoding="utf-8") as f:
        documents = json.load(f)

    logger.info("Loaded %s pages from %s sources", len(documents),
                len({d["source"] for d in documents}))

    # Show page count per source before cleaning
    source_counts: dict[str, int] = {}
    for d in documents:
        source_counts[d["source"]] = source_counts.get(d["source"], 0) + 1
    print("\nBefore cleaning — pages per source:")
    for src, count in sorted(source_counts.items()):
        print(f"  {src:<55} {count:>3} pages")

    cleaned = clean_documents(documents)

    # Show page count per source after cleaning
    clean_counts: dict[str, int] = {}
    for d in cleaned:
        clean_counts[d["source"]] = clean_counts.get(d["source"], 0) + 1
    print("\nAfter cleaning — pages per source:")
    for src, count in sorted(clean_counts.items()):
        dropped = source_counts.get(src, 0) - count
        drop_note = f"  (-{dropped} pages)" if dropped else ""
        print(f"  {src:<55} {count:>3} pages{drop_note}")

    with open(CLEAN_PATH, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=4)

    logger.info("Saved cleaned documents to %s", CLEAN_PATH)
    print(f"\nSaved to {CLEAN_PATH}")
    print("Next: update chunk_docs.py to read documents_clean.json instead of documents.json")


if __name__ == "__main__":
    main()