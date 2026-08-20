import joblib
import pandas as pd

model = joblib.load("traffic_congestion_model.pkl")

sample = pd.DataFrame({
    "road_name": ["Marine Drive"],
    "area": ["South Mumbai"],
    "weather": ["Clear"],
    "event": ["None"],
    "day_of_week": ["Monday"],
    "hour": [18],
    "avg_speed": [24],
    "vehicle_count": [620],
    "travel_time_index": [1.8],
    "month": [8],
    "day": [6],
})

prediction = model.predict(sample)

print("Predicted Congestion Level:", prediction[0])