"""
RAG configuration loader.
"""

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(slots=True)
class RAGConfig:
    embedding_model: str

    chunk_size: int
    chunk_overlap: int

    retrieval_strategy: str
    retrieval_top_k: int

    reranker_enabled: bool
    reranker_model: str
    rerank_top_k: int

    vector_store: str
    index_path: Path
    metadata_path: Path


def load_rag_config(
    config_path: str = "config/rag.yaml",
) -> RAGConfig:
    """
    Load RAG configuration from YAML.
    """

    with open(config_path, encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return RAGConfig(

        embedding_model=config["embedding"]["model"],

        chunk_size=config["chunking"]["chunk_size"],
        chunk_overlap=config["chunking"]["chunk_overlap"],

        retrieval_strategy=config["retrieval"]["strategy"],
        retrieval_top_k=config["retrieval"]["retrieval_top_k"],

        reranker_enabled=config["reranking"]["enabled"],
        reranker_model=config["reranking"]["model"],
        rerank_top_k=config["reranking"]["rerank_top_k"],

        vector_store=config["vector_store"]["type"],
        index_path=Path(config["vector_store"]["index_path"]),
        metadata_path=Path(config["vector_store"]["metadata_path"]),
    )

# """
# Configuration classes for the Unified RAG Pipeline.
# """

# from dataclasses import dataclass
# from pathlib import Path
# import yaml

# @dataclass(slots=True)
# class RAGConfig:

#     embedding_model: str

#     reranker_model: str

#     chunk_size: int
#     chunk_overlap: int

#     router_type: str              # rule | llm
#     router_enabled: bool

#     default_retriever: str

#     available_retrievers: list[str]

#     retrieval_top_k: int
#     rerank_top_k: int

#     vector_store: str

#     index_path: Path
#     metadata_path: Path