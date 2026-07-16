from dataclasses import dataclass


@dataclass
class TableDefinition:
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