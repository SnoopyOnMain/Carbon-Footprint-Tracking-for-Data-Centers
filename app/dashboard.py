import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import requests

st.set_page_config(page_title="Carbon Audit Dashboard", layout="wide")
st.title("Real-Time Green AI Audit")

# --- SYNC CONNECTION (Fixes the "Operation in Progress" Error) ---
# We use the standard postgresql driver (no +asyncpg)
DB_URL = "postgresql://postgres:Joleia#1273@db:5432/carbon_tracker_db"
engine = create_engine(DB_URL)

def get_dashboard_data():
    # We use LEFT JOIN so we don't hide logs that are missing hardware metadata
    query = """
    SELECT l.timestamp, l.power_draw_watts, COALESCE(h.name, 'Unknown Hardware') as name
    FROM fact_compute_logs l
    LEFT JOIN dim_hardware h ON l.hardware_id = h.hardware_id
    ORDER BY l.timestamp DESC
    """
    return pd.read_sql(query, engine)

# --- Sidebar: ML Prediction ---
st.sidebar.header("ML Carbon Predictor")
mins = st.sidebar.number_input("Estimated Minutes", 1, 500, 60)
if st.sidebar.button("Predict"):
    try:
        res = requests.get(f"http://web:8000/predict/{mins}").json()
        st.sidebar.metric("Predicted CO2", f"{res['predicted_co2_kg']} kg")
    except Exception as e:
        st.sidebar.error("API not reachable")

# --- Main UI ---
try:
    df = get_dashboard_data()
    
    if not df.empty:
        # 1. Metrics
        col1, col2 = st.columns(2)
        total_kwh = (df['power_draw_watts'].sum() / 3600) / 1000
        col1.metric("Total Energy Use", f"{total_kwh:.4f} kWh")
        col2.metric("CO2 Produced", f"{(total_kwh * 0.4):.4f} kg")

        # 2. Charts
        st.write("### Power Consumption Over Time (Watts)")
        st.line_chart(df.set_index('timestamp')['power_draw_watts'])
        
        # 3. Raw Data
        st.write("### Telemetry Logs")
        st.dataframe(df)
    else:
        st.info("Connected to DB, but no logs found. Run your test_emitter.py!")

except Exception as e:
    st.error(f"Waiting for database... {e}")