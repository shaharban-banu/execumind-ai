"""
Context Formatter.

Formats retrieved context into
LLM-friendly text.
"""


def format_reviews(reviews: list[dict]) -> str:
    """
    Format review retrieval results.

    Args:
        reviews:
            Retrieved reviews.

    Returns:
        str:
            Formatted reviews.
    """

    if not reviews:
        return "No customer reviews retrieved."

    formatted = []

    for index, review in enumerate(reviews, start=1):

        formatted.append(
            f"""
Review {index}

Review ID : {review["review_id"]}

Rating    : {review["review_score"]}

Review

{review["text"]}
"""
        )

    return "\n".join(formatted)


def format_business_docs(
    documents: list[dict]
) -> str:
    """
    Format retrieved business documents.

    Args:
        documents:
            Retrieved document chunks.

    Returns:
        str:
            Formatted business documents.
    """

    if not documents:
        return "No business documents retrieved."

    formatted = []

    for index, doc in enumerate(documents, start=1):

        formatted.append(
            f"""
Document {index}

Source

{doc["source"]}

Page

{doc["page"]}

Content

{doc["text"]}
"""
        )

    return "\n".join(formatted)


def format_sql_results(
    rows: list[dict]
) -> str:
    """
    Format SQL query results.

    Args:
        rows:
            SQL result rows.

    Returns:
        str:
            Formatted SQL output.
    """

    if not rows:
        return "No SQL results."

    formatted = []

    for row in rows:

        formatted.append(
            "\n".join(
                f"{k}: {v}"
                for k, v in row.items()
            )
        )

    return "\n\n".join(formatted)


def format_forecast(
    forecast: dict
) -> str:
    """
    Format forecast output.

    Args:
        forecast:
            Forecast dictionary.

    Returns:
        str:
            Formatted forecast.
    """

    if not forecast:
        return "No forecast available."

    return "\n".join(
        f"{k}: {v}"
        for k, v in forecast.items()
    )