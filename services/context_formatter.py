"""
Formatting utilities.

Provides helper functions to format retrieved documents,
SQL results, and forecast outputs for LLM prompts.
"""
from langchain_core.documents import Document
import json

def format_context(reviews: list[Document],
    business_docs: list[Document],) :
    """
    Format retrieved documents for LLM prompts.

    Args:
        reviews: Retrieved customer review documents.
        business_docs: Retrieved business documents.

    Returns:
        Formatted context string.
    """

    sections = []

    if reviews:
        sections.append("===== CUSTOMER REVIEWS =====\n")

        for i, doc in enumerate(reviews, start=1):
            sections.append(
                f"""
Review {i}

Source: {doc.metadata.get("source", "Unknown")}

Content:
{doc.page_content}
"""
            )

    if business_docs:
        sections.append("\n===== BUSINESS DOCUMENTS =====\n")

        for i, doc in enumerate(business_docs, start=1):
            sections.append(
                f"""
Document {i}

Source: {doc.metadata.get("source", "Unknown")}

Page: {doc.metadata.get("page", "-")}

Content:
{doc.page_content}
"""
            )

    if not sections:
        return "No supporting documents."

    return "\n".join(sections)
def format_sql_results(rows) -> str:
    """
    Format SQL tool output for LLM prompts.
    """

    if rows is None:
        return "No data returned."

    if isinstance(rows, str):
        return rows

    if isinstance(rows, dict):
        return json.dumps(rows, indent=2)

    if isinstance(rows, list):
        if len(rows) == 0:
            return "No records found."

        return json.dumps(rows, indent=2, default=str)

    return str(rows)


def format_forecast(forecast) -> str:
    """
    Format forecast output for LLM prompts.
    """

    if forecast is None:
        return "No forecast available."

    if isinstance(forecast, dict):
        return json.dumps(forecast, indent=2)

    if isinstance(forecast, list):
        if len(forecast) == 0:
            return "No forecast available."

        return json.dumps(forecast, indent=2, default=str)

    return str(forecast)