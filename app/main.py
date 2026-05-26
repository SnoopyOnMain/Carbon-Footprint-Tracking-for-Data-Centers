from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routes import tracking
import app.models  # Make sure the file is named models.py!

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(tracking.router)