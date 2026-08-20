"""
Train a regression model to predict Mumbai traffic congestion_level.
Run this once (locally or here) to produce models/congestion_model.pkl,
which the Streamlit app then loads for predictions.
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error, r2_score

# ---------- 1. Load data ----------
df = pd.read_csv("G:\\My Drive\\Data Science\\smartcity\\data\\traffic\\mumbai_traffic_cleaned.csv")

# ---------- 2. Feature engineering from date/time ----------
df["date"] = pd.to_datetime(df["date"])
df["hour_num"] = pd.to_datetime(df["time"], format="%H:%M:%S").dt.hour
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["dayofweek_num"] = df["date"].dt.dayofweek          # 0=Mon ... 6=Sun
df["is_weekend"] = (df["dayofweek_num"] >= 5).astype(int)

# Fill missing event with "None" (no special event that day)
df["event"] = df["event"].fillna("None")

# ---------- 3. Choose features + target ----------
numeric_features = ["month", "day", "dayofweek_num", "is_weekend", "hour_num"]
categorical_features = ["road_name", "area", "weather", "event"]
target = "congestion_level"

X = df[numeric_features + categorical_features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------- 4. Build pipeline (one-hot encode categoricals, then RandomForest) ----------
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ],
    remainder="passthrough",  # numeric_features pass through unchanged
)

model = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=200, max_depth=12, random_state=42, n_jobs=-1
    )),
])

# ---------- 5. Train ----------
model.fit(X_train, y_train)

# ---------- 6. Evaluate ----------
preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)
print(f"MAE: {mae:.2f}")
print(f"R²:  {r2:.3f}")

# ---------- 7. Save model + the list of road/area choices (for the UI dropdowns) ----------
joblib.dump(model, "models/congestion_model.pkl")


print("Saved model to congestion_model.pkl")