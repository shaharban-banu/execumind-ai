"""
ExecuMind API Routes.
"""
from datetime import datetime, timezone
import time
from fastapi import APIRouter,Form
from database.database import SessionLocal
import json
from database.models import ExecutiveRecommendation,Dataset,DatasetVersion,DatasetFile,User
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
from pandas.errors import EmptyDataError
from app.services.dataset_storage import create_dataset_version_dir
from services.executive_recommendation_generator import ExecutiveRecommendationGenerator
from services.executive_recommendation_service import ExecutiveRecommendationService
from rag.config.rag_config import load_rag_config
from forecast.services.training_service import ForecastTrainingService
from services.platform_reset import  PlatformResetService
from services.platform_status import get_platform_status
from services.active_dataset import get_active_dataset_path
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
             "history":request.history or [],
             "user_id":user.id}
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

@router.post("/datasets/upload", tags=["Dataset"])
async def upload_dataset(
    files: List[UploadFile] = File(...),
    user=Depends(get_current_user),
):
    """
    Upload a new version of the user's dataset.

    The platform maintains a single e-commerce dataset per user.
    Every upload creates a new immutable version while preserving
    all previous versions.

    Newly uploaded versions are not automatically activated or
    processed. The executive must explicitly select a version and
    run Platform Processing.

    Args:
        files: Dataset files uploaded by the user.
        user: Authenticated user.

    Returns:
        Metadata about the created dataset version.
    """
    try:
        db =SessionLocal()
        user_id=user.id
        # Find the user's only dataset
        dataset = (
            db.query(Dataset)
            .filter(Dataset.user_id == user.id)
            .first()
        )

        # First upload → create dataset
        if dataset is None:
            dataset = Dataset(
                user_id=user.id,
                name="E-Commerce Dataset",
            )
            db.add(dataset)
            db.flush()
            next_version = 1

        # Later uploads → always create next version
        else:
            latest = (
                db.query(DatasetVersion)
                .filter(DatasetVersion.dataset_id == dataset.id)
                .order_by(DatasetVersion.version_number.desc())
                .first()
            )

            next_version = (
                latest.version_number + 1
                if latest else 1
            )

        

        # ==================================================
        # 3. Create version directory
        # ==================================================

        version_dir = create_dataset_version_dir(
            user_id=user_id,
            dataset_name=dataset.name,
            version_number=next_version,
        )

        # ==================================================
        # 4. Create DatasetVersion
        # ==================================================

        version = DatasetVersion(
            dataset_id=dataset.id,
            version_number=next_version,
            status="uploaded",
            is_active=(next_version==1),
        )

        db.add(version)
        db.flush()

        uploaded_files = []

        # ==================================================
        # 5. Save files
        # ==================================================

        for file in files:

            if not file.filename:
                continue

            file_path = version_dir / file.filename

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(
                    file.file,
                    buffer,
                )

            dataset_file = DatasetFile(
                version_id=version.id,
                file_name=file.filename,
                file_path=str(file_path),
            )

            db.add(dataset_file)

            uploaded_files.append(file.filename)

            logger.info(
                "Stored '%s' in dataset '%s' version %d.",
                file.filename,
                dataset.name,
                next_version,
            )

        if not uploaded_files:
            raise HTTPException(
                status_code=400,
                detail="No valid dataset files were uploaded.",
            )

        # ==================================================
        # 6. Commit metadata
        # ==================================================

        db.commit()

        logger.info(
            "Dataset '%s' version %d uploaded successfully "
            "for user %s.",
            dataset.name,
            next_version,
            user_id,
        )

        return {
            "success": True,
            "dataset_id": dataset.id,
            "dataset_name": dataset.name,
            "version_id": version.id,
            "version": next_version,
            "status": version.status,
            "is_active": version.is_active,
            "files_uploaded": len(uploaded_files),
            "files": uploaded_files,
            "message": (
                f"Dataset version {next_version} "
                "uploaded successfully."
            ),
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()

        logger.exception(
            "Dataset upload failed."
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to upload dataset.",
        )

    finally:
        db.close()

@router.get("/datasets", tags=["Dataset"])
def get_datasets(
    user=Depends(get_current_user),
):
    """
    Return all datasets belonging to the authenticated user.

    Each dataset includes its historical versions and the
    currently active version.

    Returns:
        A list of user-owned datasets with version metadata.
    """

    db = SessionLocal()

    try:
        

        db_user =user

        if db_user is None:
            raise HTTPException(
                status_code=401,
                detail="Authenticated user was not found.",
            )

        datasets = (
            db.query(Dataset)
            .filter(
                Dataset.user_id == db_user.id
            )
            .order_by(Dataset.created_at.desc())
            .all()
        )

        result = []

        for dataset in datasets:

            versions = (
                db.query(DatasetVersion)
                .filter(
                    DatasetVersion.dataset_id == dataset.id
                )
                .order_by(
                    DatasetVersion.version_number.desc()
                )
                .all()
            )

            version_data = []

            for version in versions:

                files = (
                    db.query(DatasetFile)
                    .filter(
                        DatasetFile.version_id == version.id
                    )
                    .all()
                )

                version_data.append(
                    {
                        "id": version.id,
                        "version": version.version_number,
                        "status": version.status,
                        "is_active": version.is_active,
                        "created_at": version.created_at.isoformat(),
                        "files": [
                            {
                                "id": file.id,
                                "name": file.file_name,
                                "path": file.file_path,
                            }
                            for file in files
                        ],
                    }
                )

            result.append(
                {
                    "id": dataset.id,
                    "name": dataset.name,
                    "created_at": dataset.created_at.isoformat(),
                    "versions": version_data,
                }
            )

        return result

    finally:
        db.close()

@router.post(
    "/datasets/{dataset_id}/versions/{version_id}/activate",
    tags=["Dataset"],
)
def activate_dataset_version(
    dataset_id: int,
    version_id: int,
    user=Depends(get_current_user),
):
    """
    Activate a specific dataset version for the authenticated user.

    The selected version remains active until the user explicitly
    selects another version.

    Args:
        dataset_id: ID of the dataset.
        version_id: ID of the version to activate.
        user: Authenticated JWT user.

    Returns:
        Activated dataset and version information.
    """

    db = SessionLocal()

    try:
        

        db_user =user

        if db_user is None:
            raise HTTPException(
                status_code=401,
                detail="Authenticated user was not found.",
            )

        dataset = (
            db.query(Dataset)
            .filter(
                Dataset.id == dataset_id,
                Dataset.user_id == db_user.id,
            )
            .first()
        )

        if dataset is None:
            raise HTTPException(
                status_code=404,
                detail="Dataset not found.",
            )

        version = (
            db.query(DatasetVersion)
            .filter(
                DatasetVersion.id == version_id,
                DatasetVersion.dataset_id == dataset.id,
            )
            .first()
        )

        if version is None:
            raise HTTPException(
                status_code=404,
                detail="Dataset version not found.",
            )

        # Deactivate all versions of this dataset.
        db.query(DatasetVersion).filter(
            DatasetVersion.dataset_id == dataset.id
        ).update(
            {"is_active": False},
            synchronize_session=False,
        )

        version.is_active = True
        version.status = "ready"

        db.commit()

        return {
            "success": True,
            "dataset_id": dataset.id,
            "dataset_name": dataset.name,
            "version_id": version.id,
            "version": version.version_number,
            "is_active": True,
            "message": (
                f"Dataset version {version.version_number} "
                "is now active."
            ),
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()

        logger.exception(
            "Failed to activate dataset version."
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to activate dataset version.",
        )

    finally:
        db.close()

# @router.post("/datasets/upload", tags=["Dataset"])
# async def upload_dataset(files: List[UploadFile] = File(...),user=Depends(get_current_user),):
#     upload_dir = "data/dataset"
#     os.makedirs(upload_dir, exist_ok=True)
#     logger.info("ExecuMind CI/CD deployment test - v1")
#     uploaded_files = []

#     for file in files:
#         file_path = os.path.join(upload_dir, file.filename)

#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         uploaded_files.append(file.filename)
#     reset_service.reset()

#     return {
#         "success": True,
#         "files_uploaded": len(uploaded_files),
#         "files": uploaded_files,
#         "message": "Dataset uploaded successfully."
#     }

# @router.get("/datasets", tags=["Dataset"])
# def get_datasets(user=Depends(get_current_user)):
#     """
#     Return metadata for all uploaded datasets.
#     """

#     dataset_dir = Path("data/dataset")

#     if not dataset_dir.exists():
#         return []

#     datasets = []

#     SUPPORTED_EXTENSIONS = {
#         ".csv",
#         ".xlsx",
#         ".xls",
#         ".json",
#     }

#     for file in dataset_dir.iterdir():

#         # Skip directories
#         if not file.is_file():
#             continue

#         # Skip .gitkeep and unsupported files
#         if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
#             continue

#         # Skip empty files
#         if file.stat().st_size == 0:
#             logger.warning("Skipping empty dataset: %s", file.name)
#             continue

#         try:

#             # Load dataset
#             if file.suffix.lower() == ".csv":
#                 df = pd.read_csv(file)

#             elif file.suffix.lower() in [".xlsx", ".xls"]:
#                 df = pd.read_excel(file)

#             elif file.suffix.lower() == ".json":
#                 df = pd.read_json(file)

#             else:
#                 continue

#         except EmptyDataError:
#             logger.warning("Skipping empty dataset: %s", file.name)
#             continue

#         except Exception as e:
#             logger.exception(
#                 "Failed to read dataset %s: %s",
#                 file.name,
#                 str(e),
#             )
#             continue

#         total_cells = df.shape[0] * df.shape[1]

#         missing_cells = int(df.isna().sum().sum())

#         quality = (
#             round((1 - missing_cells / total_cells) * 100, 2)
#             if total_cells > 0
#             else 100
#         )

#         preview = []

#         for column in df.columns:

#             non_null = df[column].dropna()

#             preview.append(
#                 {
#                     "column": column,
#                     "type": str(df[column].dtype),
#                     "sample": (
#                         str(non_null.iloc[0])
#                         if not non_null.empty
#                         else ""
#                     ),
#                 }
#             )

#         datasets.append(
#             {
#                 "id": file.stem,
#                 "name": file.name,
#                 "type": file.suffix.replace(".", "").upper(),
#                 "rows": len(df),
#                 "columns": len(df.columns),
#                 "quality": quality,
#                 "status": "ready",
#                 "uploadedAt": datetime.fromtimestamp(
#                     file.stat().st_mtime
#                 ).isoformat(),
#                 "size": f"{file.stat().st_size / (1024 * 1024):.2f} MB",
#                 "preview": preview,
#             }
#         )

#     return datasets

@router.post("/datasets/process", tags=["Dataset"])
def process_dataset(user=Depends(get_current_user),):

    dataset_path=get_active_dataset_path(user_id=user.id)
    result = pipeline.run(str(dataset_path))

    return result

@router.post("/platform/process", tags=["Platform"])
def process_platform(user=Depends(get_current_user),):
    logger.info("Starting ETL...")
    dataset_path=get_active_dataset_path(user.id)
    ingestion_result=pipeline.run(str(dataset_path),user_id=user.id)

    # Stop if ETL failed
    if not ingestion_result["success"]:
        return {
            "success": False,
            "stage": "ingestion",
            "error": ingestion_result,
        }

    try:
        logger.info("Starting forecast training...")
        forecast_result = forecast_service.train(user.id)
    except Exception as exc:
        return {
            "success": False,
            "stage": "forecast",
            "error": str(exc),
        }

    try:
        logger.info("Starting RAG indexing...")
        rag_result = index_service.build_index(user.id)
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


# def get_platform_status(user_id: int):

#     model_dir = Path(f"data/users/{user_id}/models")
#     forecast_ready = all([
#         (model_dir / "revenue.pkl").exists(),
#         (model_dir / "orders.pkl").exists(),
#         (model_dir / "customers.pkl").exists(),
#         (model_dir / "aov.pkl").exists(),
#     ])

#     vector_dir = Path(f"data/users/{user_id}/vectorstore")

#     rag_ready = (
#         (vector_dir / "faiss.index").exists()
#         and (vector_dir / "metadata.pkl").exists()
#     )

#     db = SessionLocal()

#     dataset_ready = (
#         db.query(DatasetVersion)
#         .join(Dataset)
#         .filter(
#             Dataset.user_id == user_id,
#             DatasetVersion.is_active == True,
#         )
#         .first()
#         is not None
#     )

#     db.close()

#     return {
#         "dataset_ready": dataset_ready,
#         "forecast_ready": forecast_ready,
#         "rag_ready": rag_ready,
#         "platform_ready": (
#             dataset_ready and forecast_ready and rag_ready
#         ),
#     }
@router.get("/platform/status", tags=["Platform"])
def platform_status(user=Depends(get_current_user)):
    return get_platform_status(user.id)

@router.get("/forecast/{metric}",tags=["Forecast"],response_model=ForecastResponse,)
def forecast(metric:str,user=Depends(get_current_user),):

    status = get_platform_status(user.id)

    if not status["platform_ready"]:
        raise HTTPException(
            status_code=400,
            detail="Platform has not been processed. Please process the platform first.",
        )
    
    data=predictor.predict(user_id=user.id,metric=metric)
    return {
        "metric":metric.title(),
        **data,
        
    }

@router.post("/platform/reprocess", tags=["Platform"])
def reprocess_platform(user=Depends(get_current_user)):
    """
    Rebuild the platform from the currently uploaded datasets
    and knowledge documents.

    Clears:
    - PostgreSQL processed data
    - Forecast models
    - Forecast reports
    - FAISS vector store

    Keeps:
    - Uploaded datasets
    - Knowledge documents
    """

    logger.info("Starting platform reprocess...")

    # --------------------------------------------------
    # 1. Clear existing processed platform data
    # --------------------------------------------------

    try:
        reset_service.reset_for_reprocess(user.id)
    except Exception as exc:
        logger.exception("Platform reset failed.")

        return {
            "success": False,
            "stage": "reset",
            "error": str(exc),
        }

    # --------------------------------------------------
    # 2. Run ETL
    # --------------------------------------------------

    try:
        logger.info("Starting ETL after reprocess...")

        dataset_path=get_active_dataset_path(user.id)

        ingestion_result = pipeline.run(str(dataset_path))

        if not ingestion_result.get("success"):
            return {
                "success": False,
                "stage": "ingestion",
                "error": ingestion_result,
            }

    except Exception as exc:
        logger.exception("ETL failed during reprocess.")

        return {
            "success": False,
            "stage": "ingestion",
            "error": str(exc),
        }

    # --------------------------------------------------
    # 3. Train forecasting models
    # --------------------------------------------------

    try:
        logger.info("Starting forecast training...")

        forecast_result = forecast_service.train(user.id)

    except Exception as exc:
        logger.exception(
            "Forecast training failed during reprocess."
        )

        return {
            "success": False,
            "stage": "forecast",
            "error": str(exc),
        }

    # --------------------------------------------------
    # 4. Build RAG index
    # --------------------------------------------------

    try:
        logger.info("Starting RAG indexing...")

        rag_result = index_service.build_index(user.id)

        logger.info("RAG indexing finished.")

    except Exception as exc:
        logger.exception(
            "RAG indexing failed during reprocess."
        )

        return {
            "success": False,
            "stage": "knowledge",
            "error": str(exc),
        }

    # --------------------------------------------------
    # 5. Success
    # --------------------------------------------------

    logger.info("Platform reprocess completed successfully.")

    return {
        "success": True,
        "platform_status": "ready",
        "message": "Platform reprocessed successfully.",
        "ingestion": ingestion_result,
        "forecast": forecast_result,
        "knowledge": rag_result,
    }

@router.post("/platform/factory-reset", tags=["Platform"])
def factory_reset(user=Depends(get_current_user)):
    """
    Completely reset platform data.

    Deletes uploaded datasets, knowledge documents,
    processed PostgreSQL data and generated intelligence artifacts.

    Authentication data is preserved.
    """

    logger.info("Starting factory reset request.")

    try:
        reset_service.factory_reset(user.id)

        return {
            "success": True,
            "platform_status": "reset",
            "message": "Factory reset completed successfully.",
        }

    except Exception as exc:
        logger.exception("Factory reset failed.")

        return {
            "success": False,
            "stage": "factory_reset",
            "error": str(exc),
        }

@router.get("/dashboard",tags=["Dashboard"],response_model=DashboardResponse,)
def dashboard(user=Depends(get_current_user),):

    kpis = dashboard_service.get_dashboard(user.id)

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
            .filter(ExecutiveRecommendation.user_id==user.id)
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

    history = DashboardService.get_revenue_history(user.id)

    return {
        "history": history
    }

@router.post("/executive/generate",tags=["Executive Advisor"],)
def generate_recommendations(user=Depends(get_current_user),):
    generator=ExecutiveRecommendationGenerator()
    response=generator.generate(user.id)
    return response

@router.get("/executive/recommendations",tags=["Executive Advisor"],)
def get_recommendations(user=Depends(get_current_user),):

    service = ExecutiveRecommendationService()

    return service.get_recommendations(user.id)

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
            .filter(ExecutiveRecommendation.user_id==user.id)
            .order_by(ExecutiveRecommendation.created_at.desc())
            .first()
        )

        report_time = (
            latest_report.created_at.isoformat()
            if latest_report
            else datetime.now().isoformat()
        )

        # Dataset Uploaded
        if DashboardService.dataset_uploaded(user.id):
            activities.append({
                "id": "1",
                "label": "Dataset Uploaded",
                "detail": "Dataset files uploaded successfully.",
                "timestamp": report_time,
                "type": "upload",
                "actor": "Dataset Scanner",
            })

        # ETL Completed
        if DashboardService.dataset_processed(user.id):
            activities.append({
                "id": "2",
                "label": "Dataset Processed",
                "detail": "Dataset transformed into standardized business tables.",
                "timestamp": report_time,
                "type": "agent",
                "actor": "Dataset-Agnostic ETL",
            })

        # Forecast Ready
        if DashboardService.forecast_ready(user.id):
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
            .filter(ExecutiveRecommendation.user_id == user.id)
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
                if DashboardService.dataset_uploaded(user.id)
                else "down"
            ),
            "detail": (
                "Loaded successfully"
                if DashboardService.dataset_uploaded(user.id)
                else "No dataset uploaded"
            ),
        })

        # ETL Pipeline
        status.append({
            "id": "etl",
            "label": "ETL Pipeline",
            "status": (
                "operational"
                if DashboardService.dataset_processed(user.id)
                else "degraded"
            ),
            "detail": (
                "Processing completed"
                if DashboardService.dataset_processed(user.id)
                else "Waiting for processing"
            ),
        })

        # Forecast
        status.append({
            "id": "forecast",
            "label": "Forecast Agent",
            "status": (
                "operational"
                if DashboardService.forecast_ready(user.id)
                else "degraded"
            ),
            "detail": (
                "Forecast model available"
                if DashboardService.forecast_ready(user.id)
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
            .filter(ExecutiveRecommendation.user_id == user.id)
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