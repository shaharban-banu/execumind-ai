from datetime import datetime
from pydantic import BaseModel


class DatasetVersionResponse(BaseModel):
    id: int
    version_number: int
    file_name: str
    status: str
    created_at: datetime


class DatasetResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    versions: list[DatasetVersionResponse]