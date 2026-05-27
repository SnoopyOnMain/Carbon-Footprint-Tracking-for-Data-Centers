import pandas as pd

class CarbonPredictor:
    def __init__(self):
        # Grams of CO2 per kWh (Average grid intensity)
        self.co2_intensity_factor = 0.411 

    def predict_run(self, estimated_minutes: int, current_power_watts: float):
        """
        Calculates predicted CO2 based on the actual live power draw.
        Formula: (Watts * Hours) / 1000 = kWh
        """
        # Convert minutes to hours
        hours = estimated_minutes / 60
        
        # Calculate Energy in kWh
        predicted_kwh = (current_power_watts * hours) / 1000
        
        # Calculate CO2 in kg
        prediction = predicted_kwh * self.co2_intensity_factor
        
        return round(prediction, 4)

# Instantiate for use
predictor = CarbonPredictor()