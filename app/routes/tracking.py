from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
# Always start from 'app.'
from app.database import get_db
from app.models import ComputeLog
from app.schemas import ComputeLogCreate

router = APIRouter()

@router.post("/log-compute")
async def log_compute(log: ComputeLogCreate, db: AsyncSession = Depends(get_db)):
    # 1. Map the incoming JSON to our SQL Model
    db_log = ComputeLog(
        job_id=log.job_id,
        hardware_id=log.hardware_id,
        power_draw_watts=log.power_draw_watts
    )
    
    # 2. Save to Postgres
    db.add(db_log)
    await db.commit()
    
    return {"status": "saved_to_db", "job_id": log.job_id}