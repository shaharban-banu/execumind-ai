"""
ExecuMind API Routes.
"""
from datetime import datetime, timezone
import time
from fastapi import APIRouter
from database.database import SessionLocal
import json
from database.models import ExecutiveRecommendation
from app.api.schemas import (
    QuestionRequest,
    HealthResponse,AskResponse,ForecastResponse,DashboardResponse,OutOfContextResponse
)
from forecast.predict import ForecastPredictor
from app.services.dashboard_service import DashboardService
from graph.workflow import build_graph
from fastapi import UploadFile, File, HTTPException,Depends
import os
import shutil
from typing import List,Union
from pathlib import Path
from datetime import datetime
from ingestion.pipeline import IngestionPipeline
from rag.services.index_service import IndexService
import pandas as pd

from services.executive_recommendation_generator import ExecutiveRecommendationGenerator
from services.executive_recommendation_service import ExecutiveRecommendationService
from rag.config.rag_config import load_rag_config
from forecast.services.training_service import ForecastTrainingService
from services.platform_reset import  PlatformResetService
from services.platform_status import get_platform_status
from app.auth.dependencies import get_current_user
from utils.logger import logger

router = APIRouter()
graph = build_graph()
predictor = ForecastPredictor()
dashboard_service = DashboardService()
pipeline = IngestionPipeline()
index_service = IndexService()
forecast_service = ForecastTrainingService()
reset_service = PlatformResetService()


@router.get("/health",tags=["System"],summary="Health Check",response_model=HealthResponse,)
def health():
    """
    Health check.
    """
    return {
        "status": "healthy"
    }


@router.post("/ask",tags=["Executive Intelligence"],summary="Ask a business question",response_model=Union[AskResponse,OutOfContextResponse],)
def ask(request: QuestionRequest,user=Depends(get_current_user),):
    """
    Execute the ExecuMind workflow.
    """
    start = time.perf_counter()
    state = {"question": request.question,
             "history":request.history or [],}
    result = graph.invoke(state)
    if result.get("status") == "out_of_context":
        return {
            "status": "out_of_context",
            "message": result["message"],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
            },
        }
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
def forecast(metric:str,user=Depends(get_current_user),):

    status = platform_status()

    if not status["platform_ready"]:
        raise HTTPException(
            status_code=400,
            detail="Platform has not been processed. Please process the platform first.",
        )
    
    data=predictor.predict(metric)
    return {
        "metric":metric.title(),
        **data,
        
    }

@router.post("/datasets/upload", tags=["Dataset"])
async def upload_dataset(files: List[UploadFile] = File(...),user=Depends(get_current_user),):
    upload_dir = "dataset"
    os.makedirs(upload_dir, exist_ok=True)

    uploaded_files = []

    for file in files:
        file_path = os.path.join(upload_dir, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append(file.filename)
    reset_service.reset()

    return {
        "success": True,
        "files_uploaded": len(uploaded_files),
        "files": uploaded_files,
        "message": "Dataset uploaded successfully."
    }

@router.get("/datasets", tags=["Dataset"])
def get_datasets(user=Depends(get_current_user),):
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
def process_dataset(user=Depends(get_current_user),):

    result = pipeline.run("dataset")

    return result

@router.post("/platform/process", tags=["Platform"])
def process_platform(user=Depends(get_current_user),):
    logger.info("Starting ETL...")
    ingestion_result=pipeline.run("dataset")

    # Stop if ETL failed
    if not ingestion_result["success"]:
        return {
            "success": False,
            "stage": "ingestion",
            "error": ingestion_result,
        }

    try:
        logger.info("Starting forecast training...")
        forecast_result = forecast_service.train()
    except Exception as exc:
        return {
            "success": False,
            "stage": "forecast",
            "error": str(exc),
        }

    try:
        logger.info("Starting RAG indexing...")
        rag_result = index_service.build_index()
        logger.info("RAG indexing finished.")
    except Exception as exc:
        return {
            "success": False,
            "stage": "knowledge",
            "error": str(exc),
        }

    return {
        "success": True,
        "platform_status": "ready",
        "ingestion": ingestion_result,
        "forecast":forecast_result,
        "knowledge": rag_result,
    }

@router.get("/platform/status", tags=["Platform"])
def platform_status(user=Depends(get_current_user),):
    
    #db_ready = Path("data/execumind.db").exists()

    forecast_ready = all([
        Path("forecast/models/revenue.pkl").exists(),
        Path("forecast/models/orders.pkl").exists(),
        Path("forecast/models/customers.pkl").exists(),
        Path("forecast/models/aov.pkl").exists(),
    ])

    rag_config = load_rag_config()

    rag_ready = (
        rag_config.index_path.exists()
        and rag_config.metadata_path.exists()
    )

    dataset_dir = Path("dataset")

    dataset_ready = any(dataset_dir.iterdir()) if dataset_dir.exists() else False

    platform_ready = (
        dataset_ready
        and forecast_ready
        and rag_ready
    )


    return {
    "dataset_ready": dataset_ready,
    "forecast_ready": forecast_ready,
    "rag_ready": rag_ready,
    "platform_ready": (
        dataset_ready
        and forecast_ready
        and rag_ready
    ),
}

@router.get("/dashboard",tags=["Dashboard"],response_model=DashboardResponse,)
def dashboard(user=Depends(get_current_user),):

    kpis = dashboard_service.get_dashboard()

    return {
        "kpis": kpis,
        "system": {
            "database": "Connected",
            "forecast_models": "Ready",
            "vector_store": "Loaded",
        },
    }

@router.get("/dashboard/summary",tags=["Dashboard"],summary="Executive dashboard summary")
def dashboard_summary(user=Depends(get_current_user),):

    db = SessionLocal()

    try:
        latest = (
            db.query(ExecutiveRecommendation)
            .order_by(ExecutiveRecommendation.created_at.desc())
            .first()
        )

        if not latest:
            return {
                "executive_summary": "No executive report available.",
                "opportunity": "",
                "risk": "",
                "recommendation": {
                    "priority": "N/A",
                    "action": "",
                    "rationale": "",
                },
                "metadata": {},
            }

        findings = json.loads(latest.key_findings)
        risks = json.loads(latest.business_risks)

        return {
            "executive_summary": latest.executive_summary,

            "opportunity": (
                findings[0]
                if findings
                else "No opportunities identified."
            ),

            "risk": (
                risks[0]
                if risks
                else "No major risks identified."
            ),

            "recommendation": {
                "priority": latest.priority,
                "action": latest.action,
                "rationale": latest.rationale,
            },

            "metadata": {
                "generated_at": latest.created_at.isoformat(),
                "dataset_loaded": True,
                "report_ready": True,
            },
        }

    finally:
        db.close()

@router.get(
    "/dashboard/revenue-history",
    tags=["Dashboard"],
    summary="Monthly revenue history"
)
def revenue_history(user=Depends(get_current_user),):

    history = DashboardService.get_revenue_history()

    return {
        "history": history
    }

@router.post("/executive/generate",tags=["Executive Advisor"],)
def generate_recommendations(user=Depends(get_current_user),):
    generator=ExecutiveRecommendationGenerator()
    response=generator.generate()
    return response

@router.get("/executive/recommendations",tags=["Executive Advisor"],)
def get_recommendations(user=Depends(get_current_user),):

    service = ExecutiveRecommendationService()

    return service.get_recommendations()

@router.get(
    "/dashboard/activity",
    tags=["Dashboard"],
    summary="Recent executive activity",
)
def dashboard_activity(user=Depends(get_current_user),):

    db = SessionLocal()

    try:
        activities = []

        # Executive report (if available)
        latest_report = (
            db.query(ExecutiveRecommendation)
            .order_by(ExecutiveRecommendation.created_at.desc())
            .first()
        )

        report_time = (
            latest_report.created_at.isoformat()
            if latest_report
            else datetime.now().isoformat()
        )

        # Dataset Uploaded
        if DashboardService.dataset_uploaded():
            activities.append({
                "id": "1",
                "label": "Dataset Uploaded",
                "detail": "Dataset files uploaded successfully.",
                "timestamp": report_time,
                "type": "upload",
                "actor": "Dataset Scanner",
            })

        # ETL Completed
        if DashboardService.dataset_processed():
            activities.append({
                "id": "2",
                "label": "Dataset Processed",
                "detail": "Dataset transformed into standardized business tables.",
                "timestamp": report_time,
                "type": "agent",
                "actor": "Dataset-Agnostic ETL",
            })

        # Forecast Ready
        if DashboardService.forecast_ready():
            activities.append({
                "id": "3",
                "label": "Revenue Forecast Generated",
                "detail": "Forecast model trained and ready for prediction.",
                "timestamp": report_time,
                "type": "forecast",
                "actor": "Forecast Agent",
            })

        # Executive Report Ready
        if latest_report:
            activities.append({
                "id": "4",
                "label": "Executive Intelligence Report Generated",
                "detail": "Executive recommendations prepared successfully.",
                "timestamp": latest_report.created_at.isoformat(),
                "type": "decision",
                "actor": "Executive Agent",
            })

        return activities

    finally:
        db.close()

@router.get(
    "/dashboard/status",
    tags=["Dashboard"],
    summary="Current platform status",
)
def dashboard_status(user=Depends(get_current_user),):

    db = SessionLocal()

    try:
        latest_report = (
            db.query(ExecutiveRecommendation)
            .order_by(ExecutiveRecommendation.created_at.desc())
            .first()
        )

        status = []

        # Dataset
        status.append({
            "id": "dataset",
            "label": "Dataset",
            "status": (
                "operational"
                if DashboardService.dataset_uploaded()
                else "down"
            ),
            "detail": (
                "Loaded successfully"
                if DashboardService.dataset_uploaded()
                else "No dataset uploaded"
            ),
        })

        # ETL Pipeline
        status.append({
            "id": "etl",
            "label": "ETL Pipeline",
            "status": (
                "operational"
                if DashboardService.dataset_processed()
                else "degraded"
            ),
            "detail": (
                "Processing completed"
                if DashboardService.dataset_processed()
                else "Waiting for processing"
            ),
        })

        # Forecast
        status.append({
            "id": "forecast",
            "label": "Forecast Agent",
            "status": (
                "operational"
                if DashboardService.forecast_ready()
                else "degraded"
            ),
            "detail": (
                "Forecast model available"
                if DashboardService.forecast_ready()
                else "Platform not processed"
            ),
        })

        # Executive Advisor
        status.append({
            "id": "executive",
            "label": "Executive Advisor",
            "status": (
                "operational"
                if latest_report
                else "degraded"
            ),
            "detail": (
                "Latest report available"
                if latest_report
                else "Waiting for report generation"
            ),
        })
        
        return status

    finally:
        db.close()   

@router.get(
    "/dashboard/briefing",
    tags=["Dashboard"],
    summary="Executive briefing preview",
)
def executive_briefing(user=Depends(get_current_user),):
    db = SessionLocal()

    try:
        latest = (
            db.query(ExecutiveRecommendation)
            .order_by(ExecutiveRecommendation.created_at.desc())
            .first()
        )

        if not latest:
            return {
                "summary": None,
                "recommendation": None,
                "risk": None,
                "report_available": False,
            }

        return {
            "summary": latest.executive_summary,
            "risk": json.loads(latest.business_risks)[0]
                    if latest.business_risks else None,
            "recommendation": latest.action,
            "report_available": True,
        }

    finally:
        db.close()