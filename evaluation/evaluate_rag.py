"""
RAG Evaluation Module.

Evaluates retrieval performance using a
golden evaluation dataset.
"""
from utils.logger import logger
from pathlib import Path
import pandas as pd
from mcp.tools.search_docs import search_docs

DATASET_PATH=Path("evaluation/rag_evaluation_dataset.csv")
OUTPUT_DIR=Path("evaluation/results")
OUTPUT_PATH=(OUTPUT_DIR/"rag_evaluation_report.csv")

def evaluate_rag():
    """Evaluate retrieval performance"""
    try:
        df=pd.read_csv(DATASET_PATH)

        logger.info("Dataset Loaded.Contain %s questions",len(df))

        results=[]

        top1=0
        top3=0
        for _,row in df.iterrows():
            question=row['question']
            expected_source=row['expected_source']
            retrieval_results=search_docs(query=question)
            retrieved_sources=[]

            #reviews
            if expected_source=="reviews":
                if len(retrieval_results['reviews'])>0:
                    retrieved_sources.append("reviews")

            #business documents
            for result in retrieval_results['business_docs']:
                retrieved_sources.append(result['source'])
            
            retrieved_sources=list(dict.fromkeys(retrieved_sources))

            top1_hit=False
            top3_hit=False
            if len(retrieved_sources)>0:
                if (retrieved_sources[0]==expected_source):
                    top1+=1
                    top1_hit=True
            if expected_source in retrieved_sources[:3]:
                top3_hit=True
                top3+=1
            results.append({
                'question':question,
                'expected_source':expected_source,
                'retrieved_sources':"|".join(retrieved_sources),
                'top1':"PASS" if top1_hit else "FAIL",
                'top3':"PASS" if top3_hit else "FAIL"
            })
        OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
        report_df=pd.DataFrame(results)
        report_df.to_csv(OUTPUT_PATH,index=False)

        total_questions=len(df)
        top1_accuracy=round((top1/total_questions)*100,2)
        top3_accuracy=round((top3/total_questions)*100,2)

        print("\nRAG EVALUATION")
        print("="*50)

        print(f"Total Questions : {total_questions}")
        print(f"Top1 Accuracy : {top1_accuracy}")
        print(f"Top3 Accuracy : {top3_accuracy}")

        print(f"\nReport saved to {OUTPUT_PATH}")
    except Exception:
        logger.exception("Evaluation failed")
        raise

if __name__=="__main__":
    evaluate_rag()



