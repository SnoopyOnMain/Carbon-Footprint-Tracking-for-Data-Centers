from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from app.database import engine, Base, get_db  # Added engine and Base imports here
from app.predictor import predictor
from app.services.audit import create_prediction_entry, reconcile_latest_prediction
from app.models import ComputeLog, PredictionAudit
from pydantic import BaseModel
import uuid

app = FastAPI()

# --- AUTOMATIC TABLE CREATION ON STARTUP ---
@app.on_event("startup")
async def startup_event():
    """Forces PostgreSQL to create the prediction_audit table if it doesn't exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# --- Schema for the Telemetry Emitter ---
class TelemetryPayload(BaseModel):
    power_draw_watts: float
    hardware_id: int = 1  # Default fallback if emitter doesn't send it
    job_id: str = "default-job"

@app.post("/log-compute")
async def log_compute(payload: TelemetryPayload, db: AsyncSession = Depends(get_db)):
    """Accepts real-time hardware telemetry streams from test_emitter.py"""
    try:
        new_log = ComputeLog(
            job_id=payload.job_id,
            hardware_id=payload.hardware_id,
            power_draw_watts=payload.power_draw_watts
        )
        db.add(new_log)
        await db.commit()
        return {"status": "success", "logged": payload.power_draw_watts}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Logging Error: {e}")

@app.get("/predict/{minutes}")
async def predict(minutes: int, db: AsyncSession = Depends(get_db)):
    # 1. Fetch the most recent telemetry data point for the prediction engine
    try:
        result = await db.execute(
            select(ComputeLog.power_draw_watts)
            .order_by(ComputeLog.timestamp.desc())
            .limit(1)
        )
        row = result.scalar_one_or_none()
        current_power = float(row) if row is not None else 250.0
    except Exception as e:
        print(f"Prediction Query Error: {e}")
        current_power = 250.0

    # 2. DATA DRIFT DETECTION LOGIC
    drift_detected = False
    try:
        # Fetch the last 10 entries to check current distribution behavior
        drift_result = await db.execute(
            select(ComputeLog.power_draw_watts)
            .order_by(ComputeLog.timestamp.desc())
            .limit(10)
        )
        recent_logs = drift_result.scalars().all()
        
        if len(recent_logs) >= 5:
            rolling_avg_power = sum(recent_logs) / len(recent_logs)
            historical_baseline = 250.0  # Our expected model baseline configuration
            drift_threshold = 150.0      # Maximum expected fluctuation bounds
            
            # If the baseline has drifted significantly up or down, trip the alert flag
            if abs(rolling_avg_power - historical_baseline) > drift_threshold:
                drift_detected = True
                print(f"⚠️ DATA DRIFT DETECTED! Rolling Avg: {rolling_avg_power:.2f}W vs Baseline: {historical_baseline}W")
    except Exception as drift_err:
        print(f"Failed to calculate data drift metrics: {drift_err}")

    # 3. Generate the prediction calculation metrics
    prediction = predictor.predict_run(minutes, current_power)
    
    # 4. Document the forecast footprint entry inside our audit tables trail
    try:
        mock_job_id = f"job-{uuid.uuid4().hex[:8]}" 
        await create_prediction_entry(db, mock_job_id, minutes, prediction)
    except Exception as audit_err:
        print(f"Failed to log to prediction_audit table: {audit_err}")
    
    return {
        "estimated_minutes": minutes,
        "predicted_co2_kg": prediction,
        "based_on_current_draw": current_power,
        "drift_detected": drift_detected  # <--- Relays status straight to our UI
    }

@app.post("/analytics/reconcile")
async def trigger_reconcile(db: AsyncSession = Depends(get_db)):
    updated_record = await reconcile_latest_prediction(db)
    if not updated_record:
        return {"status": "skipped", "message": "No new predictions to reconcile or missing telemetry logs."}
    return {"status": "success", "reconciled_id": updated_record.id, "error_margin": updated_record.error_margin}