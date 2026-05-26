# app/dashboard.py
import asyncio
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import ComputeLog, Hardware 

async def get_job_summary(target_job_id: str):
    async with AsyncSessionLocal() as session:
        query = (
            select(ComputeLog, Hardware)
            .join(Hardware, ComputeLog.hardware_id == Hardware.hardware_id)
            .where(ComputeLog.job_id == target_job_id)
        )
        
        result = await session.execute(query)
        rows = result.all()

        if not rows:
            print(f"No data found for Job ID: {target_job_id}")
            return

        # Use row[0] for the log data and row[1] for hardware info
        _, hw_info = rows[0]
        
        # 1. Calculate energy first
        # We use float() just to be 100% sure Python doesn't treat it as an object
        total_watts = sum(float(row[0].power_draw_watts) for row in rows)
        total_kwh = (total_watts / 3600) / 1000
        
        # 2. Calculate cost and carbon
        electricity_rate = 0.16 
        total_cost = float(total_kwh) * electricity_rate
        carbon_footprint = float(total_kwh) * 0.4
        
        # 3. Print the final report
        print(f"\n--- CARBON & COST REPORT ---")
        print(f"Job ID: {target_job_id}")
        print(f"Hardware: {hw_info.name} ({hw_info.type})")
        print(f"Total Logs: {len(rows)}")
        print(f"Total Energy: {total_kwh:.6f} kWh")
        print(f"Estimated Cost: ${total_cost:.6f}") # Changed to .6f to see small values!
        print(f"CO2 Emissions: {carbon_footprint:.6f} kg")
        print(f"-----------------------------\n")

if __name__ == "__main__":
    # Ensure this matches a Job ID currently in your pgAdmin
    job_to_check = "8efe9c45" 
    asyncio.run(get_job_summary(job_to_check))