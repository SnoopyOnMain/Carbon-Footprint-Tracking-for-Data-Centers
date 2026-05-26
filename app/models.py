from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Hardware(Base):
    __tablename__ = "dim_hardware"
    
    # Use mapped_column for everything to stay consistent
    hardware_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=True)
    tdp_watts: Mapped[float] = mapped_column(Float, nullable=True)

class ComputeLog(Base):
    __tablename__ = "fact_compute_logs"
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String, index=True)
    hardware_id = Column(Integer) # For now, we'll keep it simple
    power_draw_watts = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())