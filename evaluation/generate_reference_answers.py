import pickle
import pandas as pd

from services.llm_service import LLMService


# Load evaluation dataset
dataset = pd.read_csv("evaluation/evaluation_dataset_1.csv")

# Load stored chunks
with open("data/vectorstore/metadata.pkl", "rb") as f:
    documents = pickle.load(f)

# Create lookup: chunk_id -> Document
chunk_lookup = {
    str(doc.metadata["chunk_id"]): doc
    for doc in documents
}

llm = LLMService()

reference_answers = []

for _, row in dataset.iterrows():

    question = row["question"]

    chunk_ids = [
        x.strip()
        for x in row["relevant_chunk_ids"].split(";")
    ]

    contexts = []

    for chunk_id in chunk_ids:

        if chunk_id in chunk_lookup:

            contexts.append(
                chunk_lookup[chunk_id].page_content
            )
    contexts = list(dict.fromkeys(contexts))
    context_text = "\n\n".join(contexts)
    prompt = f"""
You are creating a gold-standard reference answer for evaluating a
Retrieval-Augmented Generation (RAG) system.

Question:
{question}

Relevant Context:
{context_text}

Instructions:

1. Answer ONLY using the supplied context.
2. Do not add outside knowledge.
3. Write 2-4 concise sentences.
4. Combine repeated information.
5. Do not mention "the context" or "the document".
6. Return ONLY the answer.
"""

    response = llm.generate_text(
        prompt=prompt,
    )

    reference_answers.append(response)

dataset["reference_answer"] = reference_answers

dataset.to_csv(
    "evaluation/evaluation_dataset_with_reference.csv",
    index=False,
)

print("Reference answers generated.")