import pandas as pd

from rag.services.pipeline_service import create_pipeline

TOP_K = 10


def reciprocal_rank(retrieved_ids, relevant_ids):
    """
    Compute Reciprocal Rank.
    """
    for rank, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in relevant_ids:
            return 1 / rank
    return 0.0


def evaluate():

    pipeline = create_pipeline()

    dataset = pd.read_csv("evaluation/evaluation_dataset_1.csv")

    recall_scores = []
    precision_scores = []
    hit_scores = []
    mrr_scores = []

    for _, row in dataset.iterrows():

        question = row["question"]

        relevant_ids = {
            x.strip()
            for x in str(row["relevant_chunk_ids"]).split(";")
        }

        docs = pipeline.retrieve(
            query=question,
            retrieval_top_k=TOP_K,
            rerank_top_k=TOP_K,
        )

        retrieved_ids = [
            str(doc.metadata["chunk_id"])
            for doc in docs
        ]

        hits = len(
            set(retrieved_ids) & relevant_ids
        )

        recall = hits / len(relevant_ids) if relevant_ids else 0.0

        precision = hits / len(retrieved_ids) if retrieved_ids else 0.0

        hit_rate = 1 if hits > 0 else 0

        mrr = reciprocal_rank(
            retrieved_ids,
            relevant_ids,
        )

        recall_scores.append(recall)
        precision_scores.append(precision)
        hit_scores.append(hit_rate)
        mrr_scores.append(mrr)

        print("=" * 80)
        print(question)
        print("Relevant :", relevant_ids)
        print("Retrieved:", retrieved_ids)
        print(f"Recall@{TOP_K}: {recall:.2f}")
        print(f"Precision@{TOP_K}: {precision:.2f}")
        print(f"MRR: {mrr:.2f}")

    print("\n")
    print("=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    print(f"Recall@{TOP_K}:    {sum(recall_scores)/len(recall_scores):.3f}")
    print(f"Precision@{TOP_K}: {sum(precision_scores)/len(precision_scores):.3f}")
    print(f"Hit Rate@{TOP_K}:  {sum(hit_scores)/len(hit_scores):.3f}")
    print(f"MRR:               {sum(mrr_scores)/len(mrr_scores):.3f}")


if __name__ == "__main__":
    evaluate()