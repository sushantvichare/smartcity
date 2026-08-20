
# aqi_prediction_model.py

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import joblib


# ============================================================
# 1. LOAD DATA
# ============================================================

FILE_PATH = "air_quality_historical.csv"

df = pd.read_csv(r"G:\My Drive\Data Science\smartcity\data\aqi\air_quality_historical.csv")

# Convert date
df["date"] = pd.to_datetime(
    df["date"],
    format="%d-%m-%Y",
    errors="coerce"
)

# Sort chronologically
df = df.sort_values("date").reset_index(drop=True)


# ============================================================
# 2. SELECT AQI TARGET
# ============================================================

# We are predicting US AQI
df = df[["date", "us_aqi"]].dropna()

df = df.sort_values("date").reset_index(drop=True)


# ============================================================
# 3. CREATE TIME-SERIES FEATURES
# ============================================================

# Previous AQI values
for lag in [1, 2, 3, 7, 14, 30]:
    df[f"aqi_lag_{lag}"] = df["us_aqi"].shift(lag)


# Rolling averages
for window in [3, 7, 14, 30]:
    df[f"aqi_rolling_{window}"] = (
        df["us_aqi"]
        .shift(1)
        .rolling(window)
        .mean()
    )


# Calendar features
df["day"] = df["date"].dt.day
df["month"] = df["date"].dt.month
df["day_of_week"] = df["date"].dt.dayofweek
df["day_of_year"] = df["date"].dt.dayofyear
df["year"] = df["date"].dt.year


# Seasonal features
df["doy_sin"] = np.sin(
    2 * np.pi * df["day_of_year"] / 365.25
)

df["doy_cos"] = np.cos(
    2 * np.pi * df["day_of_year"] / 365.25
)


# Remove rows created by lag/rolling calculations
df = df.dropna().reset_index(drop=True)


# ============================================================
# 4. FEATURES AND TARGET
# ============================================================

FEATURES = [
    "aqi_lag_1",
    "aqi_lag_2",
    "aqi_lag_3",
    "aqi_lag_7",
    "aqi_lag_14",
    "aqi_lag_30",

    "aqi_rolling_3",
    "aqi_rolling_7",
    "aqi_rolling_14",
    "aqi_rolling_30",

    "day",
    "month",
    "day_of_week",
    "day_of_year",
    "year",

    "doy_sin",
    "doy_cos"
]

X = df[FEATURES]
y = df["us_aqi"]


# ============================================================
# 5. TIME-BASED TRAIN/TEST SPLIT
# ============================================================

# DO NOT randomly shuffle time-series data

split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


# ============================================================
# 6. TRAIN RANDOM FOREST
# ============================================================

model = RandomForestRegressor(
    n_estimators=400,
    max_depth=12,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# ============================================================
# 7. EVALUATE MODEL
# ============================================================

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("=" * 50)
print("AQI MODEL PERFORMANCE")
print("=" * 50)

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.2f}")


# ============================================================
# 8. PREDICT AQI FOR A FUTURE DATE
# ============================================================

def predict_aqi(target_date, history):
    """
    Predict AQI for a future date.

    target_date : string/date
    history     : DataFrame containing date and us_aqi
    """

    target_date = pd.to_datetime(target_date)

    history = history.copy()
    history["date"] = pd.to_datetime(history["date"])

    history = history.sort_values("date")

    aqi_values = history["us_aqi"].dropna().tolist()

    # Need at least 30 previous AQI values
    if len(aqi_values) < 30:
        raise ValueError(
            "At least 30 historical AQI records are required."
        )

    # Previous AQI values
    features = {}

    features["aqi_lag_1"] = aqi_values[-1]
    features["aqi_lag_2"] = aqi_values[-2]
    features["aqi_lag_3"] = aqi_values[-3]
    features["aqi_lag_7"] = aqi_values[-7]
    features["aqi_lag_14"] = aqi_values[-14]
    features["aqi_lag_30"] = aqi_values[-30]

    # Rolling averages
    features["aqi_rolling_3"] = np.mean(aqi_values[-3:])
    features["aqi_rolling_7"] = np.mean(aqi_values[-7:])
    features["aqi_rolling_14"] = np.mean(aqi_values[-14:])
    features["aqi_rolling_30"] = np.mean(aqi_values[-30:])

    # Date features
    day_of_year = target_date.dayofyear

    features["day"] = target_date.day
    features["month"] = target_date.month
    features["day_of_week"] = target_date.dayofweek
    features["day_of_year"] = day_of_year
    features["year"] = target_date.year

    # Seasonal features
    features["doy_sin"] = np.sin(
        2 * np.pi * day_of_year / 365.25
    )

    features["doy_cos"] = np.cos(
        2 * np.pi * day_of_year / 365.25
    )

    # Convert to DataFrame
    input_data = pd.DataFrame([features])

    # Make prediction
    prediction = model.predict(
        input_data[FEATURES]
    )[0]

    return round(prediction, 2)






joblib.dump(
    model,
    "models/aqi_prediction_model.pkl"
)

print()
print("Model saved as: aqi_prediction_model.pkl")

