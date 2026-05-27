from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routes import tracking
import app.models  # Make sure the file is named models.py!
from app.predictor import predictor


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(tracking.router)


@app.get("/predict/{minutes}")
async def get_prediction(minutes: int):
    # The predictor is a normal class, so no await needed here
    estimated_co2 = predictor.predict_run(minutes)
    return {
        "estimated_minutes": minutes,
        "predicted_co2_kg": estimated_co2,
        "recommendation": "Go ahead!" if estimated_co2 < 1.0 else "Consider waiting for off-peak hours."
    }