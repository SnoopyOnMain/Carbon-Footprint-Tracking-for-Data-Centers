from pydantic import BaseModel, Field
from datetime import datetime

class ComputeLogCreate(BaseModel):
    job_id: str
    hardware_id: int
    power_draw_watts: float = Field(..., gt=0) # Must be greater than 0
    timestamp: datetime = Field(default_factory=datetime.now)

class ModelRunCreate(BaseModel):
    model_name: str
    user_id: str
    region: str = "us-east-1"