import os
import joblib
import pandas as pd
import numpy as np


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)


# ============================================================
# MODEL PATHS
# ============================================================

TRAFFIC_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "congestion_model.pkl"
)

AQI_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "aqi_prediction_model.pkl"
)

COMPLAINT_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "citizen_satisfaction_model.pkl"
)


# ============================================================
# DATA PATHS
# ============================================================

TRAFFIC_DATA_PATH = os.path.join(
    DATA_DIR,
    "traffic",
    "traffic_cleaned.csv"
)



COMPLAINT_DATA_PATH = os.path.join(
    DATA_DIR,
    "complaints",
    "complaints_cleaned.csv"
)


# ============================================================
# MODEL LOADER
# ============================================================

def load_model(path):
    """
    Load sklearn model using Joblib.
    """

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model not found: {path}"
        )

    return joblib.load(path)


# ============================================================
# DATA LOADER
# ============================================================

def load_data(path):
    """
    Load CSV dataset.
    """

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    return pd.read_csv(path)


# ============================================================
# ============================================================
# TRAFFIC
# ============================================================
# ============================================================

def predict_traffic(
    area,
    road_name,
    date,
    hour,
    weather="Clear",
    event="None"
):
    """
    Predict traffic congestion.

    Required model features:

    road_name
    area
    day
    month
    hour_num
    dayofweek_num
    is_weekend
    weather
    event
    """

    try:

        model = load_model(
            TRAFFIC_MODEL_PATH
        )

        # ----------------------------------------------------
        # Date
        # ----------------------------------------------------

        date = pd.to_datetime(date)

        day = date.day
        month = date.month
        dayofweek_num = date.dayofweek

        is_weekend = int(
            dayofweek_num >= 5
        )

        # ----------------------------------------------------
        # Prepare input
        # ----------------------------------------------------

        input_data = pd.DataFrame({

            "road_name": [road_name],

            "area": [area],

            "day": [day],

            "month": [month],

            "hour_num": [hour],

            "dayofweek_num": [dayofweek_num],

            "is_weekend": [is_weekend],

            "weather": [weather],

            "event": [event]
        })

        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        prediction = model.predict(
            input_data
        )

        congestion = float(
            prediction[0]
        )

        # ----------------------------------------------------
        # Estimate speed
        # ----------------------------------------------------

        avg_speed = max(
            5,
            60 - (
                congestion * 0.45
            )
        )

        return {

            "area": area,

            "road_name": road_name,

            "date": date.strftime(
                "%Y-%m-%d"
            ),

            "hour": hour,

            "weather": weather,

            "event": event,

            "congestion_level": round(
                congestion,
                2
            ),

            "avg_speed": round(
                avg_speed,
                2
            )
        }

    except Exception as e:

        return {
            "error": str(e),
            "tool": "predict_traffic"
        }

# ============================================================
# ============================================================
# AQI
# ============================================================
# ============================================================

def get_aqi_category(aqi):
    """
    Convert AQI value to category.
    """

    if aqi <= 50:
        return "Good"

    elif aqi <= 100:
        return "Satisfactory"

    elif aqi <= 200:
        return "Moderate"

    elif aqi <= 300:
        return "Poor"

    elif aqi <= 400:
        return "Very Poor"

    else:
        return "Severe"


def predict_aqi(date):
    """
    Predict AQI using ONLY the target date.

    Model features:

        day
        month
        day_of_week
        day_of_year
        year
        doy_sin
        doy_cos
    """

    try:

        # ----------------------------------------------------
        # Load model
        # ----------------------------------------------------

        model = load_model(
            AQI_MODEL_PATH
        )

        # ----------------------------------------------------
        # Convert date
        # ----------------------------------------------------

        target_date = pd.to_datetime(
            date,
            errors="coerce"
        )

        if pd.isna(target_date):

            return {
                "error": "Invalid date provided.",
                "tool": "predict_aqi"
            }

        # ----------------------------------------------------
        # Extract date features
        # ----------------------------------------------------

        day = target_date.day

        month = target_date.month

        day_of_week = target_date.dayofweek

        day_of_year = target_date.dayofyear

        year = target_date.year

        # ----------------------------------------------------
        # Seasonal features
        # ----------------------------------------------------

        doy_sin = np.sin(
            2 * np.pi * day_of_year / 365.25
        )

        doy_cos = np.cos(
            2 * np.pi * day_of_year / 365.25
        )

        # ----------------------------------------------------
        # Create model input
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # EXACT feature order used during training
        # ----------------------------------------------------

        FEATURES = [
            "day",
            "month",
            "day_of_week",
            "day_of_year",
            "year",
            "doy_sin",
            "doy_cos"
        ]

        input_data = input_data[FEATURES]

        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        prediction = model.predict(
            input_data
        )

        aqi = float(
            prediction[0]
        )

        # ----------------------------------------------------
        # Return result
        # ----------------------------------------------------

        return {
            "date": target_date.strftime(
                "%Y-%m-%d"
            ),

            "aqi": round(
                aqi,
                2
            ),

            "category": get_aqi_category(
                aqi
            )
        }

    except Exception as e:

        return {
            "error": str(e),
            "tool": "predict_aqi"
        }

# ============================================================
# ============================================================
# CITIZEN SATISFACTION
# ============================================================
# ============================================================

def predict_complaints(
    complaint_date,
    ward_code,
    ward_area,
    zone,
    ward_type,
    population_density,
    ward_slum_percentage,
    complaint_category,
    department_assigned,
    complaint_channel,
    severity,
    has_photo_evidence,
    has_gps_location,
    media_attention,
    politically_sensitive,
    complainant_type,
    property_type,
    repeat_complainant,
    prior_complaints_count,
    resolution_days,
    num_reassignments,
    complaint_status,
    contractor_category,
    work_quality_rating,
    site_inspected,
    defect_liability_claim,
    estimated_cost_inr,
    infrastructure_age_years,
    months_since_last_maintained,
    complaint_id=0
):
    """
    Predict citizen satisfaction.

    Target:

        citizen_satisfied

    The input features match the
    complaint dataset schema.
    """

    try:

        model = load_model(
            COMPLAINT_MODEL_PATH
        )

        complaint_date = pd.to_datetime(
            complaint_date
        )

        # ----------------------------------------------------
        # Date features
        # ----------------------------------------------------

        year = complaint_date.year

        month = complaint_date.month

        is_monsoon_season = int(
            month in [6, 7, 8, 9]
        )

        complaint_time_of_day = (
            complaint_date.hour
        )

        # ----------------------------------------------------
        # Prepare input
        # ----------------------------------------------------

        input_data = pd.DataFrame({

            "complaint_id": [
                complaint_id
            ],

            "complaint_date": [
                complaint_date
            ],

            "year": [year],

            "month": [month],

            "is_monsoon_season": [
                is_monsoon_season
            ],

            "complaint_time_of_day": [
                complaint_time_of_day
            ],

            "ward_code": [
                ward_code
            ],

            "ward_area": [
                ward_area
            ],

            "zone": [
                zone
            ],

            "ward_type": [
                ward_type
            ],

            "population_density": [
                population_density
            ],

            "ward_slum_percentage": [
                ward_slum_percentage
            ],

            "complaint_category": [
                complaint_category
            ],

            "department_assigned": [
                department_assigned
            ],

            "complaint_channel": [
                complaint_channel
            ],

            "severity": [
                severity
            ],

            "has_photo_evidence": [
                has_photo_evidence
            ],

            "has_gps_location": [
                has_gps_location
            ],

            "media_attention": [
                media_attention
            ],

            "politically_sensitive": [
                politically_sensitive
            ],

            "complainant_type": [
                complainant_type
            ],

            "property_type": [
                property_type
            ],

            "repeat_complainant": [
                repeat_complainant
            ],

            "prior_complaints_count": [
                prior_complaints_count
            ],

            "resolution_days": [
                resolution_days
            ],

            "num_reassignments": [
                num_reassignments
            ],

            "complaint_status": [
                complaint_status
            ],

            "contractor_category": [
                contractor_category
            ],

            "work_quality_rating": [
                work_quality_rating
            ],

            "site_inspected": [
                site_inspected
            ],

            "defect_liability_claim": [
                defect_liability_claim
            ],

            "estimated_cost_inr": [
                estimated_cost_inr
            ],

            "infrastructure_age_years": [
                infrastructure_age_years
            ],

            "months_since_last_maintained": [
                months_since_last_maintained
            ]
        })

        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        prediction = model.predict(
            input_data
        )

        result = prediction[0]

        # ----------------------------------------------------
        # Handle classification output
        # ----------------------------------------------------

        if isinstance(
            result,
            (np.integer, int)
        ):

            satisfied = bool(
                result
            )

        elif isinstance(
            result,
            (np.floating, float)
        ):

            satisfied = bool(
                round(result)
            )

        else:

            satisfied = str(
                result
            )

        # ----------------------------------------------------
        # Probability
        # ----------------------------------------------------

        probability = None

        if hasattr(
            model,
            "predict_proba"
        ):

            try:

                probabilities = (
                    model.predict_proba(
                        input_data
                    )
                )

                probability = float(
                    np.max(
                        probabilities[0]
                    )
                )

            except Exception:

                probability = None

        return {

            "complaint_category":
                complaint_category,

            "ward_area":
                ward_area,

            "prediction":
                satisfied,

            "citizen_satisfied":
                satisfied,

            "confidence":
                round(
                    probability * 100,
                    2
                )
                if probability is not None
                else None
        }

    except Exception as e:

        return {
            "error": str(e),
            "tool": "predict_complaints"
        }


# ============================================================
# MODEL TEST
# ============================================================

def test_models():

    print("\n" + "=" * 60)
    print("MODEL TEST")
    print("=" * 60)

    models = {

        "Traffic":
            TRAFFIC_MODEL_PATH,

        "AQI":
            AQI_MODEL_PATH,

        "Citizen Satisfaction":
            COMPLAINT_MODEL_PATH
    }

    for name, path in models.items():

        print(
            f"\n{name}:"
        )

        try:

            model = load_model(
                path
            )

            print(
                "[Success] Loaded successfully"
            )

            print(
                "Type:",
                type(model)
            )

            # ------------------------------------------------
            # Show expected features if available
            # ------------------------------------------------

            if hasattr(
                model,
                "feature_names_in_"
            ):

                print(
                    "Features:"
                )

                print(
                    list(
                        model.feature_names_in_
                    )
                )

        except Exception as e:

            print(
                "[FAILED] Failed"
            )

            print(
                e
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    test_models()