import datetime
from sqlalchemy import String, Integer, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Hardware(Base):
    __tablename__ = "dim_hardware"
    
    hardware_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=True)
    tdp_watts: Mapped[float] = mapped_column(Float, nullable=True)

class ComputeLog(Base):
    __tablename__ = "fact_compute_logs"
    
    log_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_id: Mapped[str] = mapped_column(String(100), index=True, nullable=True)
    hardware_id: Mapped[int] = mapped_column(Integer, nullable=True) 
    power_draw_watts: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class PredictionAudit(Base):
    __tablename__ = "prediction_audit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    predicted_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    predicted_co2_kg: Mapped[float] = mapped_column(Float, nullable=False)
    actual_co2_kg: Mapped[float] = mapped_column(Float, nullable=True) 
    error_margin: Mapped[float] = mapped_column(Float, nullable=True)