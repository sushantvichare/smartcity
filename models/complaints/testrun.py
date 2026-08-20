import pandas as pd
import joblib

model = joblib.load("citizen_satisfaction_model.pkl")

sample = pd.DataFrame({
    "Complaint_Type": ["Garbage"],
    "Ward": ["A"],
    "Area": ["Colaba"],
    "Priority": ["High"],
    "Status": ["Resolved"],
    "Resolution_Time": [2],
    "Latitude": [18.92],
    "Longitude": [72.82]
})

prediction = model.predict(sample)

print("Predicted Citizen Satisfaction:", prediction[0])