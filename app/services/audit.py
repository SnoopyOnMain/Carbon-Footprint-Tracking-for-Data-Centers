import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import PredictionAudit, ComputeLog

async def create_prediction_entry(
    db: AsyncSession, 
    job_id: str, 
    minutes: int, 
    predicted_co2: float
) -> PredictionAudit:
    """Logs the initial prediction to the database."""
    audit_entry = PredictionAudit(
        timestamp=datetime.datetime.utcnow(),
        predicted_minutes=minutes,
        predicted_co2_kg=predicted_co2,
        actual_co2_kg=None,
        error_margin=None
    )
    # Using job_id logic if you want to extend it later, 
    # but for now we write it straight to our audit table.
    db.add(audit_entry)
    await db.commit()
    await db.refresh(audit_entry)
    return audit_entry

async def reconcile_latest_prediction(db: AsyncSession, grid_intensity: float = 0.411):
    """
    Finds the latest unreconciled prediction, aggregates the actual telemetry 
    collected during that window, and evaluates the model's error margin.
    """
    # 1. Find the latest prediction that hasn't been evaluated yet
    stmt = (
        select(PredictionAudit)
        .where(PredictionAudit.actual_co2_kg == None)
        .order_by(PredictionAudit.timestamp.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    latest_prediction = result.scalar_one_or_none()
    
    if not latest_prediction:
        return None  # Nothing to reconcile
        
    # 2. Grab telemetry logs that occurred after this prediction was made
    logs_stmt = (
        select(ComputeLog)
        .where(ComputeLog.timestamp >= latest_prediction.timestamp)
        .order_by(ComputeLog.timestamp.asc())
    )
    logs_result = await db.execute(logs_stmt)
    logs = logs_result.scalars().all()
    
    if not logs:
        return None  # Wait for more telemetry to stream in
        
    # 3. Calculate true carbon consumption
    # Formula: (Average Watts * Hours) / 1000 * Grid Intensity Factor
    total_watts = sum(log.power_draw_watts for log in logs)
    avg_watts = total_watts / len(logs)
    
    # Estimate duration based on your tracking intervals (e.g., 10 seconds per log)
    total_seconds = len(logs) * 10 
    hours_run = total_seconds / 3600
    
    actual_kwh = (avg_watts * hours_run) / 1000
    actual_co2 = actual_kwh * grid_intensity
    
    # 4. Update evaluation metrics
    latest_prediction.actual_co2_kg = actual_co2
    latest_prediction.error_margin = actual_co2 - latest_prediction.predicted_co2_kg
    
    await db.commit()
    await db.refresh(latest_prediction)
    return latest_prediction