"""
RAG table definitions.

Defines the database tables and their corresponding
text and metadata columns used by the RAG loaders.
"""
from dataclasses import dataclass


@dataclass
class TableDefinition:
    """
    Configuration describing a RAG source table.

    Attributes:
        text_column: Column containing the searchable text.
        metadata_columns: Columns stored as document metadata.
    """
    text_column: str
    metadata_columns: list[str]


RAG_TABLES = {
    "reviews": TableDefinition(
        text_column="review_text",
        metadata_columns=[
            "review_id",
            "order_id",
            "review_score",
            "review_date",
        ],
    ),

    "products": TableDefinition(
        text_column="product_name",
        metadata_columns=[
            "product_id",
            "product_category",
        ],
    ),
}