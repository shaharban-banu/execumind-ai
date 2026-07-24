"""
ExecuMind API Routes.
"""
from datetime import datetime, timezone
import time
from fastapi import APIRouter

from app.api.schemas import (
    QuestionRequest,
    HealthResponse,AskResponse,ForecastResponse,DashboardResponse
)
from forecast.predict import ForecastPredictor
from app.services.dashboard_service import DashboardService
from graph.workflow import build_graph
from fastapi import UploadFile, File, HTTPException
import os
import shutil
from typing import List
from pathlib import Path
from datetime import datetime
from ingestion.pipeline import IngestionPipeline
import pandas as pd

from services.executive_recommendation_generator import ExecutiveRecommendationGenerator
from services.executive_recommendation_service import ExecutiveRecommendationService



router = APIRouter()
graph = build_graph()
predictor = ForecastPredictor()
dashboard_service = DashboardService()
pipeline = IngestionPipeline()


@router.get("/health",tags=["System"],summary="Health Check",response_model=HealthResponse,)
def health():
    """
    Health check.
    """
    return {
        "status": "healthy"
    }


@router.post("/ask",tags=["Executive Intelligence"],summary="Ask a business question",response_model=AskResponse)
def ask(request: QuestionRequest):
    """
    Execute the ExecuMind workflow.
    """
    start = time.perf_counter()
    state = {"question": request.question,}
    result = graph.invoke(state)
    elapsed_ms = int((time.perf_counter() - start) * 1000)
    planner = result["planner_decision"]
    
    return {
        "question": request.question,
        "planner": {"selected_agents": planner.selected_agents,},
        "executive_analysis": result["executive_analysis"].model_dump(),
        "metadata": {
            "execution_time_ms": elapsed_ms,
            "generated_at": datetime.now(timezone.utc),
        },
    }

@router.get("/forecast/{metric}",tags=["Forecast"],response_model=ForecastResponse,)
def forecast(metric:str):
    data=predictor.predict(metric)
    return {
        "metric":metric.title(),
        **data,
    }

@router.get("/dashboard",tags=["Dashboard"],response_model=DashboardResponse,)
def dashboard():

    kpis = dashboard_service.get_dashboard()

    return {
        "kpis": kpis,
        "system": {
            "database": "Connected",
            "forecast_models": "Ready",
            "vector_store": "Loaded",
        },
    }

@router.post("/datasets/upload", tags=["Dataset"])
async def upload_dataset(files: List[UploadFile] = File(...)):
    upload_dir = "dataset"
    os.makedirs(upload_dir, exist_ok=True)

    uploaded_files = []

    for file in files:
        file_path = os.path.join(upload_dir, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append(file.filename)

    return {
        "success": True,
        "files_uploaded": len(uploaded_files),
        "files": uploaded_files,
        "message": "Dataset uploaded successfully."
    }

@router.get("/datasets", tags=["Dataset"])
def get_datasets():
    dataset_dir = Path("dataset")

    if not dataset_dir.exists():
        return []

    datasets = []
    
    for file in dataset_dir.glob("*"):
        if file.is_file():
            df = pd.read_csv(file)
            total_cells = df.shape[0] * df.shape[1]

            missing_cells = df.isna().sum().sum()

            quality = (
                round((1 - missing_cells / total_cells) * 100, 2)
                if total_cells > 0
                else 100
            )
            datasets.append({
                "id": file.stem,
                "name": file.name,
                "type": file.suffix.replace(".", "").upper(),
                "rows": len(df),
                "columns": len(df.columns),
                "quality": quality,
                "status": "ready",
                "uploadedAt": datetime.fromtimestamp(file.stat().st_mtime).isoformat(),
                "size": f"{file.stat().st_size / 1024 / 1024:.2f} MB",
                "preview": [
                {
                    "column": column,
                    "type": str(df[column].dtype),
                    "sample": (
                        str(df[column].dropna().iloc[0])
                        if not df[column].dropna().empty
                        else ""
                    ),
                }
                for column in df.columns
                            ]
            })

    return datasets

@router.post("/datasets/process", tags=["Dataset"])
def process_dataset():

    result = pipeline.run("dataset")

    return result

# @router.get(
#     "/dashboard/summary",
#     tags=["Dashboard"],
#     summary="Executive dashboard summary"
# )
# def dashboard_summary():
#     question = (
#         "Provide a concise executive dashboard summary. "
#         "Return the top business opportunity, the biggest risk, "
#         "and one actionable recommendation."
#     )

#     start = time.perf_counter()

#     try:
#         result = graph.invoke({
#             "question": question
#         })

#     except Exception as e:
#         return {
#             "executive_summary": "Executive summary is temporarily unavailable.",
#             "opportunity": "",
#             "risk": "",
#             "recommendation": {
#                 "priority": "Info",
#                 "action": "Please try again later.",
#                 "rationale": str(e),
#             },
#         }

#     elapsed_ms = int((time.perf_counter() - start) * 1000)

#     analysis = result["executive_analysis"]
#     recommendation = (
#         analysis.strategic_recommendations[0]
#         if analysis.strategic_recommendations
#         else None
#     )
#     return {
#         "executive_summary": analysis.executive_summary,
#         "opportunity": (
#             analysis.key_findings[0]
#             if analysis.key_findings
#             else "No opportunities identified."
#         ),
#         "risk": (
#             analysis.business_risks[0]
#             if analysis.business_risks
#             else "No major risks identified."
#         ),
#         "recommendation": {
#             "priority": recommendation.priority if recommendation else "N/A",
#             "action": recommendation.action if recommendation else "No recommendations available.",
#             "rationale": recommendation.rationale if recommendation else "",
#         },
#         "metadata": {
#             "execution_time_ms": elapsed_ms,
#             "generated_at": datetime.now(timezone.utc),
#         },
#     }

@router.get(
    "/dashboard/revenue-history",
    tags=["Dashboard"],
    summary="Monthly revenue history"
)
def revenue_history():

    history = DashboardService.get_revenue_history()

    return {
        "history": history
    }

@router.post("/executive/generate",tags=["Executive Advisor"],)
def generate_recommendations():
    generator=ExecutiveRecommendationGenerator()
    response=generator.generate()
    return response

@router.get("/executive/recommendations",tags=["Executive Advisor"],)
def get_recommendations():

    service = ExecutiveRecommendationService()

    return service.get_recommendations()
