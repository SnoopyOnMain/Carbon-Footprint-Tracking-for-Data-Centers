import mlflow
import mlflow.pyfunc
import random
import time

# 1. Connect to our local Dockerized MLflow server
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Carbon_Predictor_Optimization")

def train_predictor_model():
    print("🚀 Starting training run for Carbon Predictor Engine...")
    
    with mlflow.start_run():
        # Simulate hyperparameter tuning (e.g., historical rolling window size)
        rolling_window_minutes = random.choice([15, 30, 45, 60])
        smoothing_alpha = round(random.uniform(0.1, 0.9), 2)
        
        print(f"Configuring parameters -> Window: {rolling_window_minutes}m, Alpha: {smoothing_alpha}")
        
        # Log our model parameters to MLflow
        mlflow.log_param("rolling_window_minutes", rolling_window_minutes)
        mlflow.log_param("smoothing_alpha", smoothing_alpha)
        
        # Simulate computing synthetic loss metric validations
        print("Evaluating model accuracy against historic baselines...")
        time.sleep(2)  # Simulate processing time
        
        simulated_mae = round(random.uniform(0.04, 0.15), 4)
        simulated_r2 = round(random.uniform(0.85, 0.98), 4)
        
        # Log our performance evaluation metrics
        mlflow.log_metric("MAE", simulated_mae)
        mlflow.log_metric("R2_Score", simulated_r2)
        
        # Tag the run with metadata
        mlflow.set_tag("model_type", "Exponential_Smoothing_Predictor")
        mlflow.set_tag("developer", "MLOps_Pipeline")
        
        print(f"✅ Training completed! Logged MAE: {simulated_mae}, R2: {simulated_r2}")
        print("Run tracked successfully in MLflow UI.")

if __name__ == "__main__":
    # Let's run it 3 times to generate a nice comparative history graph!
    for i in range(3):
        print(f"\n--- Run {i+1} ---")
        train_predictor_model()