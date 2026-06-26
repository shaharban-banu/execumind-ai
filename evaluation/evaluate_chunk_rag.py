"""chunk-level RAG evaluation"""
import sys
from pathlib import Path
import pandas as pd

from utils.logger import logger
from mcp.tools.search_docs import search_docs

DATASET_PATH=Path("evaluation/chunk_level_evaluation_dataset_fixed.csv")
OUTPUT_DIR=Path("evaluation/results")

def get_retrieved_chunk_ids(retrieval_results):
    """extract retrieved chunk ids"""

    chunk_ids=[]

    for review in retrieval_results['reviews']:
        #metadata=review.get("metadata",{})
        if "chunk_id" in review:
            chunk_ids.append(int(review['chunk_id']))
    for doc in retrieval_results["business_docs"]:
        if "chunk_id" in doc:
            chunk_ids.append(int(doc['chunk_id']))
    return chunk_ids

def evaluate_chunk_rag(retrieval_methods:str="faiss"):
    """evaluate chunk level retrieval"""

    try:
        df=pd.read_csv(DATASET_PATH)
        logger.info("loaded %s questions",len(df))
        
        results=[]
        primary_top1=0
        primary_top3=0
        recall3=0
        recall5=0
        mrr_sum=0

        for _,row in df.iterrows():
            question=row['question']
            question_type=row['question_type']
            expected_source=row['expected_source']
            expected_primary=int(row["expected_primary_chunk"])
            expected_chunks=[int(chunk) for chunk in str(row['expected_chunk_ids']).split('|')]

            retrieval_results=(search_docs(query=question,review_top_k=5,business_top_k=5,method=retrieval_methods))

            if question_type=="review":
                candidates=[r for r in retrieval_results['reviews'] if 'chunk_id' in r]
            else:
                candidates = [d for d in retrieval_results["business_docs"] if "chunk_id" in d]   

            retrieved_chunks=[c['chunk_id'] for c in candidates]
            retrieved_chunks=[int(c) if str(c).isdigit() else c for c in retrieved_chunks]
            #Top1------
            top1_hit=False
            if retrieved_chunks:
                if (retrieved_chunks[0]==expected_primary):
                    top1_hit=True
                    primary_top1+=1
            #top3-------
            top3_hit=False
            if (expected_primary in retrieved_chunks[:3]):
                top3_hit=True
                primary_top3+=1

            #recall3------
            recall3_hit=any(chunk in retrieved_chunks[:3] for chunk in expected_chunks)
            if recall3_hit:
                recall3+=1

            #recall5-----
            recall5_hit=any(chunk in retrieved_chunks[:5] for chunk in expected_chunks)
            if recall5_hit:
                recall5+=1

            #mrr--------
            reciprocal_rank=0.0

            for rank,chunk_id in enumerate(retrieved_chunks,start=1):
                if (chunk_id in expected_chunks):
                    reciprocal_rank=1/rank
                    break
            mrr_sum+=reciprocal_rank

            results.append({
                "question":question,
                "expected_primary":expected_primary,
                "expected_chunks":"|".join(map(str,expected_chunks)),
                "retrieved_chunks":"|".join(map(str,retrieved_chunks)),
                "top1":"PASS" if top1_hit else "FAIL",
                "top3":"PASS" if top3_hit else "FAIL",
                "recall3":"PASS" if recall3_hit else "FAIL",
                "recall5":"PASS" if recall5_hit else "FAIL",
                "mrr":reciprocal_rank,
            })
        OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
        OUTPUT_PATH=(OUTPUT_DIR/f"chunk_eval_{retrieval_methods}.csv")
        report_df=pd.DataFrame(results)
        report_df.to_csv(OUTPUT_PATH,index=False)

        total_question=len(df)
        top1_accuracy=round((primary_top1/total_question)*100,2)
        top3_accuracy=round((primary_top3/total_question)*100,2)
        recall3_accuracy=round((recall3/total_question)*100,2)
        recall5_accuracy=round((recall5/total_question)*100,2)
        mrr=round((mrr_sum/total_question),4)
        print("CHUNK LEVEL EVALUATION")
        print("-"*80)
        print(f"Method         : {retrieval_methods}")
        print(f"primary TOP1   : {top1_accuracy}")
        print(f"primary TOP3   : {top3_accuracy}")
        print(f"Recall@3       : {recall3_accuracy}")
        print(f"Recall@5       : {recall5_accuracy}")
        print(f"MRR            : {mrr}")
        print(f"Report saved to {OUTPUT_PATH}")
    except Exception:
        logger.exception("Chunk evaluation Failed...")

def compare_methods_by_type(methods=["faiss","hybrid"]):
    """Compare retrieval methods broken down by question type"""
    
    all_results = {}
    
    for method in methods:
        path = OUTPUT_DIR / f"chunk_eval_{method}.csv"
        df = pd.read_csv(path)
        all_results[method] = df
    
    question_types = ["review", "document", "executive"]
    
    for qtype in question_types:
        print(f"\n{'='*60}")
        print(f"Question type: {qtype.upper()}")
        print(f"{'='*60}")
        
        for method in methods:
            df = all_results[method]
            subset = df[df["question"].isin(
                pd.read_csv(DATASET_PATH).query(
                    "question_type == @qtype"
                )["question"]
            )]
            
            total = len(subset)
            top1 = (subset["top1"] == "PASS").sum() / total * 100
            recall3 = (subset["recall3"] == "PASS").sum() / total * 100
            mrr = subset["mrr"].mean()
            
            print(f"  {method:<10} Top1: {top1:.1f}%  Recall@3: {recall3:.1f}%  MRR: {mrr:.4f}")


if __name__=="__main__":
    method=(sys.argv[1] if len(sys.argv)>1 else "faiss")
    evaluate_chunk_rag(method)
    available = [
        m for m in ["faiss", "hybrid", "rerank"]
        if (OUTPUT_DIR / f"chunk_eval_{m}.csv").exists()
    ]
    if len(available) > 1:
        compare_methods_by_type(available)
    else:
        print(f"\nRun other methods first to enable comparison.")