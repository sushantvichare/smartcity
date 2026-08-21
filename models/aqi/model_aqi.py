# aqi_prediction_model.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os


# ============================================================
# 1. LOAD DATA
# ============================================================

FILE_PATH = r"G:\My Drive\Data Science\smartcity\data\aqi\air_quality_historical.csv"

df = pd.read_csv(FILE_PATH)


# ============================================================
# 2. CONVERT DATE
# ============================================================

df["date"] = pd.to_datetime(
    df["date"],
    format="%d-%m-%Y",
    errors="coerce"
)

df = df.dropna(subset=["date", "us_aqi"])

df = df.sort_values("date").reset_index(drop=True)


# ============================================================
# 3. CREATE FEATURES USING ONLY DATE
# ============================================================

df["day"] = df["date"].dt.day

df["month"] = df["date"].dt.month

df["day_of_week"] = df["date"].dt.dayofweek

df["day_of_year"] = df["date"].dt.dayofyear

df["year"] = df["date"].dt.year


# ============================================================
# 4. SEASONAL FEATURES
# ============================================================

df["doy_sin"] = np.sin(
    2 * np.pi * df["day_of_year"] / 365.25
)

df["doy_cos"] = np.cos(
    2 * np.pi * df["day_of_year"] / 365.25
)


# ============================================================
# 5. FEATURES AND TARGET
# ============================================================

FEATURES = [
    "day",
    "month",
    "day_of_week",
    "day_of_year",
    "year",
    "doy_sin",
    "doy_cos"
]

X = df[FEATURES]

# Dependent / target variable
y = df["us_aqi"]


# ============================================================
# 6. TIME-BASED TRAIN / TEST SPLIT
# ============================================================

split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


# ============================================================
# 7. TRAIN RANDOM FOREST
# ============================================================

model = RandomForestRegressor(
    n_estimators=400,
    max_depth=12,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)


# ============================================================
# 8. EVALUATE MODEL
# ============================================================

y_pred = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    y_pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred
    )
)

r2 = r2_score(
    y_test,
    y_pred
)


print("=" * 50)
print("AQI MODEL PERFORMANCE")
print("=" * 50)

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.2f}")


# ============================================================
# 9. PREDICTION FUNCTION
# ============================================================

def predict_aqi(target_date):
    """
    Predict AQI using ONLY the target date.

    Parameters
    ----------
    target_date : str or datetime
        Date for which AQI should be predicted.

    Returns
    -------
    float
        Predicted US AQI
    """

    # --------------------------------------------------------
    # Convert date
    # --------------------------------------------------------

    target_date = pd.to_datetime(
        target_date,
        errors="coerce"
    )

    if pd.isna(target_date):
        raise ValueError(
            "Invalid date provided."
        )


    # --------------------------------------------------------
    # Create date features
    # --------------------------------------------------------

    day = target_date.day

    month = target_date.month

    day_of_week = target_date.dayofweek

    day_of_year = target_date.dayofyear

    year = target_date.year


    # --------------------------------------------------------
    # Seasonal features
    # --------------------------------------------------------

    doy_sin = np.sin(
        2 * np.pi * day_of_year / 365.25
    )

    doy_cos = np.cos(
        2 * np.pi * day_of_year / 365.25
    )


    # --------------------------------------------------------
    # Create prediction DataFrame
    # --------------------------------------------------------

    input_data = pd.DataFrame([
        {
            "day": day,
            "month": month,
            "day_of_week": day_of_week,
            "day_of_year": day_of_year,
            "year": year,
            "doy_sin": doy_sin,
            "doy_cos": doy_cos
        }
    ])


    # --------------------------------------------------------
    # Ensure exact training feature order
    # --------------------------------------------------------

    input_data = input_data[FEATURES]


    # --------------------------------------------------------
    # Predict
    # --------------------------------------------------------

    prediction = model.predict(
        input_data
    )[0]


    return round(
        float(prediction),
        2
    )


# ============================================================
# 10. SAVE MODEL
# ============================================================

os.makedirs(
    "models",
    exist_ok=True
)

joblib.dump(
    model,
    "models/aqi_prediction_model.pkl"
)

print()
print("Model saved as: models/aqi_prediction_model.pkl")


# ============================================================
# 11. TEST PREDICTION
# ============================================================

if __name__ == "__main__":

    test_date = "21-08-2026"

    prediction = predict_aqi(
        test_date
    )

    print()
    print(
        f"Predicted AQI for {test_date}: {prediction}"
    )