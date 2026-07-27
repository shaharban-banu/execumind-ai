from pydantic import BaseModel, Field

class ReferenceAnswer(BaseModel):
    """
    Reference answer for RAG evaluation.
    """

    answer: str = Field(
        description="Concise ideal answer based only on the supplied contexts."
    )