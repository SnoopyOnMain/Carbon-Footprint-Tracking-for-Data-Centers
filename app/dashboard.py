import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import requests

st.set_page_config(page_title="Carbon Audit Dashboard", layout="wide")
initial_sidebar_state = "expanded"
st.title("Real-Time Green AI Audit")

# --- SYNC CONNECTION ---
DB_URL = "postgresql://postgres:Joleia#1273@db:5432/carbon_tracker_db"
engine = create_engine(DB_URL)

def get_dashboard_data():
    query = """
    SELECT l.timestamp, l.power_draw_watts, h.name, h.tdp_watts
    FROM fact_compute_logs l
    LEFT JOIN dim_hardware h ON l.hardware_id = h.hardware_id
    ORDER BY l.timestamp DESC
    """
    return pd.read_sql(query, engine)

# --- Sidebar: ML Prediction & Data Drift UI Integration ---
st.sidebar.header("ML Carbon Predictor")
mins = st.sidebar.number_input("Estimated Minutes", 1, 500, 60)

if st.sidebar.button("Predict"):
    try:
        # Fetch payload from FastAPI gateway
        res = requests.get(f"http://web:8000/predict/{mins}").json()
        st.sidebar.metric("Predicted CO2", f"{res['predicted_co2_kg']:.4f} kg")
        
        # --- DATA DRIFT UI FLAG TRACER ---
        if res.get("drift_detected", False):
            st.error("⚠️ **Warning: Input Data Drift Detected!** The current hardware power profile deviates significantly from historic model baselines. Prediction accuracy may degrade.")
        else:
            st.success("✅ Input data matches historical distribution bounds safely.")
            
    except Exception as e:
        st.sidebar.error(f"API not reachable: {e}")

# --- Main UI ---
try:
    df = get_dashboard_data()
    
    if not df.empty:
        # 1. Top Level Metrics
        col1, col2, col3 = st.columns(3)
        total_kwh = (df['power_draw_watts'].sum() / 3600) / 1000
        carbon_kg = total_kwh * 0.411  # Global avg intensity
        
        col1.metric("Total Energy", f"{total_kwh:.4f} kWh")
        col2.metric("Total CO2", f"{carbon_kg:.4f} kg")
        
        # SNEAKY DETAIL 1: Efficiency Logic
        avg_watts = df['power_draw_watts'].mean()
        efficiency_grade = "High" if avg_watts < 250 else "Moderate"
        col3.metric("Efficiency Grade", efficiency_grade, delta="Optimized" if avg_watts < 200 else "-Strained")

        # 2. Charts
        st.write("### Power Heartbeat (Real-Time)")
        st.area_chart(df.set_index('timestamp')['power_draw_watts'])
        
        # SNEAKY DETAIL 2: Carbon-Aware "Green Window"
        st.info("**Pro-Tip:** Moving heavy compute to 2:00 AM (EST) could reduce this job's carbon footprint by ~15% based on grid mix.")

        # 3. Raw Data
        with st.expander("See Raw Telemetry Details"):
            st.dataframe(df, use_container_width=True)
            
        # 4. Hardware Efficiency & Load Progression Bars
        latest_draw = df['power_draw_watts'].iloc[0]
        tdp = df['tdp_watts'].iloc[0] if df['tdp_watts'].iloc[0] else 300.0
        efficiency = (latest_draw / tdp) * 100

        st.write(f"### Current Hardware Load: {efficiency:.1f}%")
        st.progress(min(efficiency / 100, 1.0))

        if efficiency < 20:
            st.warning("**Under-utilized:** Your hardware is idling. Consider batching jobs to save energy.")
        elif efficiency > 95:
            st.error("**Thermal Stress:** Running near max TDP. Check cooling or optimize code.")
        else:
            st.success("**Optimal Range:** Hardware is being used efficiently.")

        # Calculate Efficiency vs TDP
        latest_watts = df['power_draw_watts'].iloc[0]
        tdp_limit = 400.0 
        utilization = (latest_watts / tdp_limit) * 100

        st.write(f"### Hardware Utilization: {utilization:.1f}%")
        st.progress(min(utilization / 100, 1.0))
        
        if utilization > 90:
            st.error("⚠️ **Thermal Warning:** Running near peak capacity!")
        elif utilization < 10:
            st.warning("⚠️ **Idle Alert:** GPU is under-utilized. Efficiency is low.")
            
    else:
        st.info("Connected to DB, but no logs found. Run your test_emitter.py!")

except Exception as e:
    st.error(f"Waiting for database... {e}")

# --- Performance Analytics Rendering ---
def show_performance_metrics(df_audit):
    st.header("Model Performance Audit")
    
    mae = df_audit['error_margin'].abs().mean()
    st.metric("Mean Absolute Error", f"{mae:.4f} kgCO2")

    chart_data = df_audit[['timestamp', 'predicted_co2_kg', 'actual_co2_kg']].set_index('timestamp')
    st.line_chart(chart_data)

    st.subheader("Significant Deviations")
    st.write(df_audit.sort_values(by='error_margin', ascending=False).head(5))

def get_audit_data():
    query = """
    SELECT timestamp, predicted_co2_kg, actual_co2_kg, error_margin 
    FROM prediction_audit 
    WHERE actual_co2_kg IS NOT NULL
    ORDER BY timestamp DESC
    """
    return pd.read_sql(query, engine)

try:
    df_audit = get_audit_data()
    if not df_audit.empty:
        st.markdown("---")
        show_performance_metrics(df_audit)
    else:
        st.info("No reconciled model evaluations found yet. Run predictions and allow telemetry to collect!")
except Exception as audit_err:
    st.error(f"Could not load performance audit data: {audit_err}")