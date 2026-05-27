import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# For now, we'll use a simple rule-based mock, 
# but as you get more data, this will learn from your DB!
class CarbonPredictor:
    def __init__(self):
        self.model = LinearRegression()
        # Average grams of CO2 per minute for an A100 at full load
        self.co2_per_min_a100 = 0.5 

    def predict_run(self, estimated_minutes: int):
        prediction = estimated_minutes * self.co2_per_min_a100
        return round(prediction, 4)

# Instantiate for use
predictor = CarbonPredictor()