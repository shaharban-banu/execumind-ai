from langchain_core.documents import Document
import json

def format_context(documents: list[Document],) :
    """
    Format retrieved context.
    """

    if not documents:
        return "No supporting documents."

    formatted = []

    for index, doc in enumerate(documents,start=1,):

        source = doc.metadata.get("source","Unknown",)

        page = doc.metadata.get("page","-")

        formatted.append(
            f"""
            Document {index}

            Source: {source}

            Page: {page}

            Content:
            {doc.page_content}
            """
                    )

    return "\n".join(formatted)

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