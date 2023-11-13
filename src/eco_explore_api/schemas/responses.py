from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class HealthCheckResponse(BaseModel):
    message: Optional[str] = ""
    time: Optional[datetime] = datetime.now()


class VersionResponse(BaseModel):
    version: float
    detail: HealthCheckResponse
