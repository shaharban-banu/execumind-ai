"""
ExecuMind API Routes.
"""

from fastapi import APIRouter

from app.api.schemas import (
    QuestionRequest,
    HealthResponse,
)

from graph.workflow import build_graph

router = APIRouter()
graph = build_graph()

@router.get("/health",tags=["System"],summary="Health Check",response_model=HealthResponse,)
def health():
    """
    Health check.
    """
    return {
        "status": "healthy"
    }


@router.post("/ask",tags=["Executive Intelligence"],summary="Ask a business question",)
def ask(request: QuestionRequest):
    """
    Execute the ExecuMind workflow.
    """

    state = {
        "question": request.question,
    }

    result = graph.invoke(state)

    return {
        "planner": result["planner_decision"],
        "executive_analysis": result["executive_analysis"],
    }