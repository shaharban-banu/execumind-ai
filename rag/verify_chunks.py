"""
RAG Chunk Verification Script.

Run this after chunk_reviews.py and chunk_docs.py
to confirm both pipelines produced correct output.

Usage:
    python -m rag.verify_chunks

Expected results:
    Review chunks : ~40,000 - 41,000
    Empty review chunks : 0
    Doc chunks    : ~130 - 140
    Empty doc chunks    : 0
    Duplicate chunk_ids : 0
"""

import json
from pathlib import Path
from utils.logger import logger

REVIEW_CHUNK_PATH = Path("rag/reviews/chunks/review_chunks.json")
DOC_CHUNK_PATH    = Path("rag/docs/chunks/doc_chunks.json")

PASS = "  ✓ PASS"
FAIL = "  ✗ FAIL"


# --------------------------------------------------
# Review chunk verification
# --------------------------------------------------

def verify_review_chunks() -> bool:
    """
    Verify review chunks are correctly formed.

    Checks:
        1. File exists
        2. Total chunk count is between 38,000 and 45,000
        3. No chunks have empty text
        4. No chunks have 'nan' as text
        5. All required keys are present
        6. review_score is always 1-5
    """
    print("\n" + "=" * 60)
    print("REVIEW CHUNKS")
    print("=" * 60)

    all_passed = True

    # Check 1 — file exists
    if not REVIEW_CHUNK_PATH.exists():
        print(f"{FAIL}  File not found: {REVIEW_CHUNK_PATH}")
        print("       Run chunk_reviews.py first")
        return False

    with open(REVIEW_CHUNK_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"\n  Total chunks loaded : {len(chunks)}")

    # Check 2 — count in expected range
    # 41% of 99,224 reviews have text = ~40,950
    if 38_000 <= len(chunks) <= 45_000:
        print(f"{PASS}  Chunk count {len(chunks)} is in expected range (38k-45k)")
    else:
        print(f"{FAIL}  Chunk count {len(chunks)} is OUTSIDE expected range (38k-45k)")
        print(f"       If count is ~99,000 your nan filter is not working")
        print(f"       If count is 0 your database query returned nothing")
        all_passed = False

    # Check 3 — no empty text
    empty = [c for c in chunks if not str(c.get("text", "")).strip()]
    if len(empty) == 0:
        print(f"{PASS}  No empty text chunks")
    else:
        print(f"{FAIL}  {len(empty)} chunks have empty text")
        print(f"       Sample: {empty[:2]}")
        all_passed = False

    # Check 4 — no nan text
    nan_chunks = [c for c in chunks if str(c.get("text", "")).lower() == "nan"]
    if len(nan_chunks) == 0:
        print(f"{PASS}  No 'nan' text chunks")
    else:
        print(f"{FAIL}  {len(nan_chunks)} chunks have 'nan' as text")
        print(f"       Your nan filter in chunk_reviews.py is not working")
        all_passed = False

    # Check 5 — required keys
    required_keys = {"review_id", "order_id", "review_score", "text"}
    missing_keys = [
        c for c in chunks[:100]
        if not required_keys.issubset(c.keys())
    ]
    if len(missing_keys) == 0:
        print(f"{PASS}  All required keys present: {required_keys}")
    else:
        print(f"{FAIL}  Some chunks missing required keys")
        print(f"       Expected: {required_keys}")
        print(f"       Found: {set(chunks[0].keys())}")
        all_passed = False

    # Check 6 — review scores valid
    invalid_scores = [
        c for c in chunks
        if not isinstance(c.get("review_score"), int)
        or not (1 <= c["review_score"] <= 5)
    ]
    if len(invalid_scores) == 0:
        print(f"{PASS}  All review scores are valid integers 1-5")
    else:
        print(f"{FAIL}  {len(invalid_scores)} chunks have invalid review_score")
        print(f"       Sample: {invalid_scores[:2]}")
        all_passed = False

    # Score distribution — informational
    scores = [c["review_score"] for c in chunks]
    dist = {s: scores.count(s) for s in sorted(set(scores))}
    print(f"\n  Score distribution:")
    for score, count in dist.items():
        bar = "█" * (count // 1000)
        pct = round(count / len(chunks) * 100, 1)
        print(f"    {score} star : {count:>6} ({pct}%)  {bar}")

    # Sample — informational
    print(f"\n  Sample chunk:")
    sample = chunks[0]
    print(f"    review_id    : {sample['review_id']}")
    print(f"    order_id     : {sample['order_id']}")
    print(f"    review_score : {sample['review_score']}")
    print(f"    text preview : {sample['text'][:120]}")

    return all_passed


# --------------------------------------------------
# Doc chunk verification
# --------------------------------------------------

def verify_doc_chunks() -> bool:
    """
    Verify business document chunks are correctly formed.

    Checks:
        1. File exists
        2. Total chunk count is between 100 and 200
        3. No chunks have empty text
        4. chunk_ids are unique (no duplicates from bug)
        5. chunk_ids are sequential starting from 1
        6. All 6 source documents are represented
        7. All required keys are present
    """
    print("\n" + "=" * 60)
    print("BUSINESS DOC CHUNKS")
    print("=" * 60)

    all_passed = True

    # Check 1 — file exists
    if not DOC_CHUNK_PATH.exists():
        print(f"{FAIL}  File not found: {DOC_CHUNK_PATH}")
        print("       Run chunk_docs.py first")
        return False

    with open(DOC_CHUNK_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"\n  Total chunks loaded : {len(chunks)}")

    # Check 2 — count in expected range
    # 6 PDFs at 700 char chunks → expect 100-200 chunks
    if 100 <= len(chunks) <= 200:
        print(f"{PASS}  Chunk count {len(chunks)} is in expected range (100-200)")
    else:
        print(f"{FAIL}  Chunk count {len(chunks)} is OUTSIDE expected range (100-200)")
        print(f"       If too low: some PDFs may have failed to extract text")
        print(f"       If too high: check CHUNK_SIZE setting (should be 700)")
        all_passed = False

    # Check 3 — no empty text
    empty = [c for c in chunks if not str(c.get("text", "")).strip()]
    if len(empty) == 0:
        print(f"{PASS}  No empty text chunks")
    else:
        print(f"{FAIL}  {len(empty)} chunks have empty text")
        all_passed = False

    # Check 4 — unique chunk_ids (catches the bug)
    ids = [c["chunk_id"] for c in chunks]
    unique_ids = set(ids)
    if len(unique_ids) == len(ids):
        print(f"{PASS}  All chunk_ids are unique ({len(unique_ids)} unique)")
    else:
        duplicates = len(ids) - len(unique_ids)
        print(f"{FAIL}  {duplicates} duplicate chunk_ids found")
        print(f"       chunk_id is incrementing per document not per chunk")
        print(f"       Fix: move chunk_id += 1 inside the inner for loop")
        all_passed = False

    # Check 5 — sequential from 1
    if ids[0] == 1 and ids[-1] == len(chunks):
        print(f"{PASS}  chunk_ids are sequential: 1 to {len(chunks)}")
    else:
        print(f"{FAIL}  chunk_ids are NOT sequential")
        print(f"       First: {ids[0]}  Last: {ids[-1]}  Total: {len(chunks)}")
        all_passed = False

    # Check 6 — all sources represented
    sources = {}
    for c in chunks:
        s = c["source"]
        sources[s] = sources.get(s, 0) + 1

    expected_sources = {
        "olist_company_overview",
        "olist_business_strategy",
        "olist_executive_playbook",
        "consumer_behavior",
        "ecommerce_analysis",
        "2025_PCMI_Brazil-E-commerce-Data-Portrait_EN",
    }

    found_sources = set(sources.keys())
    missing_sources = expected_sources - found_sources

    print(f"\n  Chunks per source document:")
    for src, count in sorted(sources.items()):
        print(f"    {src:<55} {count:>3} chunks")

    if len(missing_sources) == 0:
        print(f"{PASS}  All 6 source documents are represented")
    else:
        print(f"{FAIL}  Missing sources: {missing_sources}")
        print(f"       Check rag/docs/raw_docs/ for these PDF files")
        all_passed = False

    # Check 7 — required keys
    required_keys = {"chunk_id", "source", "page", "text"}
    missing_keys = [
        c for c in chunks[:20]
        if not required_keys.issubset(c.keys())
    ]
    if len(missing_keys) == 0:
        print(f"{PASS}  All required keys present: {required_keys}")
    else:
        print(f"{FAIL}  Some chunks missing required keys")
        print(f"       Expected: {required_keys}")
        print(f"       Found: {set(chunks[0].keys())}")
        all_passed = False

    # Sample — informational
    print(f"\n  Sample chunk:")
    sample = chunks[0]
    print(f"    chunk_id : {sample['chunk_id']}")
    print(f"    source   : {sample['source']}")
    print(f"    page     : {sample['page']}")
    print(f"    text     : {sample['text'][:120]}")

    return all_passed


# --------------------------------------------------
# Entry point
# --------------------------------------------------

def main() -> None:

    print("\n" + "=" * 60)
    print("ExecuMind AI — RAG Chunk Verification")
    print("=" * 60)

    review_ok = verify_review_chunks()
    doc_ok    = verify_doc_chunks()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Review chunks : {'PASS ✓' if review_ok else 'FAIL ✗'}")
    print(f"  Doc chunks    : {'PASS ✓' if doc_ok    else 'FAIL ✗'}")

    if review_ok and doc_ok:
        print("\n  All checks passed. Ready for Week 3.")
    else:
        print("\n  Fix the issues above before starting Week 3.")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()