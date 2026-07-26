"""
API request/response schemas.
"""
from datetime import datetime
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class HealthResponse(BaseModel):
    status: str

class PlannerResponse(BaseModel):
    selected_agents: list[str]


class MetadataResponse(BaseModel):
    execution_time_ms: int
    generated_at: datetime


class AskResponse(BaseModel):
    question: str
    planner: PlannerResponse
    executive_analysis: dict
    metadata: MetadataResponse

class ForecastPoint(BaseModel):
    date: str
    prediction: float
    lower_bound: float
    upper_bound: float


class ForecastConfidenceResponse(BaseModel):
    level: str
    score: int
    summary: str
    evaluation_method: str

class ForecastEvaluationMetrics(BaseModel):
    MAE: float
    RMSE: float
    MAPE: float

class ForecastValidationResponse(BaseModel):
    status: str
    method: str
    metrics: ForecastEvaluationMetrics

class HistoricalPoint(BaseModel):
    date: str
    value: float

class ForecastInsights(BaseModel):
    trend: str
    risk: str
    recommendation: str


class ForecastResponse(BaseModel):
    metric: str
    history: list[HistoricalPoint]
    forecast: list[ForecastPoint]
    confidence: ForecastConfidenceResponse
    validation: ForecastValidationResponse
    insights: ForecastInsights

class DashboardKPIs(BaseModel):
    revenue: float
    orders: int
    customers: int
    average_order_value: float


class SystemStatus(BaseModel):
    database: str
    forecast_models: str
    vector_store: str


class DashboardResponse(BaseModel):
    kpis: DashboardKPIs
    system: SystemStatus