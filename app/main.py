from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import engine, Base, get_db
from app.predictor import predictor

app = FastAPI()

@app.get("/predict/{minutes}")
async def predict(minutes: int, db: AsyncSession = Depends(get_db)): # Use AsyncSession
    try:
        # We await the execution and then the fetching
        result = await db.execute(text(
            "SELECT power_draw_watts FROM fact_compute_logs ORDER BY timestamp DESC LIMIT 1"
        ))
        row = result.fetchone()
        
        current_power = float(row[0]) if row else 250.0
        
    except Exception as e:
        print(f"Prediction Query Error: {e}")
        current_power = 250.0
    
    prediction = predictor.predict_run(minutes, current_power)
    
    return {
        "estimated_minutes": minutes,
        "predicted_co2_kg": prediction,
        "based_on_current_draw": current_power
    }