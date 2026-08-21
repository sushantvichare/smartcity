import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import sys


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data"
)

MODEL_DIR = os.path.join(
    PROJECT_ROOT,
    "models"
)

# Add project root to Python path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ============================================================
# IMPORT CHATBOT
# ============================================================

from chatbot.agent import SmartCityAgent

# Keep agent in Streamlit session
if "agent" not in st.session_state:
    st.session_state.agent = SmartCityAgent()

agent = st.session_state.agent
# ============================================================
# PAGE
# ============================================================

st.title("🏠 Smart City Dashboard")


# ============================================================
# LOAD AQI MODEL
# ============================================================

AQI_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "aqi_prediction_model.pkl"
)

try:
    aqi_model = joblib.load(AQI_MODEL_PATH)
except Exception as e:
    aqi_model = None
    st.error(f"Could not load AQI model: {e}")


# ============================================================
# AQI PREDICTION FUNCTION
# ============================================================

def predict_aqi(target_date):

    if aqi_model is None:
        return None

    target_date = pd.to_datetime(
        target_date,
        errors="coerce"
    )

    if pd.isna(target_date):
        return None

    day = target_date.day
    month = target_date.month
    day_of_week = target_date.dayofweek
    day_of_year = target_date.dayofyear
    year = target_date.year

    doy_sin = np.sin(
        2 * np.pi * day_of_year / 365.25
    )

    doy_cos = np.cos(
        2 * np.pi * day_of_year / 365.25
    )

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

    # Make sure columns match training
    input_data = input_data[
        [
            "day",
            "month",
            "day_of_week",
            "day_of_year",
            "year",
            "doy_sin",
            "doy_cos"
        ]
    ]

    prediction = aqi_model.predict(
        input_data
    )[0]

    return round(float(prediction), 2)


# ============================================================
# LOAD TRAFFIC DATA
# ============================================================

TRAFFIC_DIR = os.path.join(
    DATA_DIR,
    "traffic"
)

# Change this to your actual CSV filename
TRAFFIC_FILE = os.path.join(
    TRAFFIC_DIR,
    "mumbai_traffic_cleaned.csv"
)


@st.cache_data
def load_traffic():

    df = pd.read_csv(
        TRAFFIC_FILE
    )

    df["datetime"] = pd.to_datetime(
        df["datetime"],
        errors="coerce"
    )

    return df


try:

    traffic_df = load_traffic()

except Exception as e:

    traffic_df = pd.DataFrame()

    st.warning(
        f"Traffic data could not be loaded: {e}"
    )


# ============================================================
# TODAY
# ============================================================

today = pd.Timestamp.today().normalize()


# ============================================================
# TODAY'S TRAFFIC
# ============================================================

if not traffic_df.empty:

    today_traffic = traffic_df[
        traffic_df["datetime"].dt.normalize()
        == today
    ]

    # If today's data doesn't exist,
    # use the latest available date.

    if today_traffic.empty:

        latest_date = (
            traffic_df["datetime"]
            .dt.normalize()
            .max()
        )

        today_traffic = traffic_df[
            traffic_df["datetime"].dt.normalize()
            == latest_date
        ]

        traffic_date_label = (
            f"Latest available: "
            f"{latest_date.strftime('%d-%m-%Y')}"
        )

    else:

        traffic_date_label = (
            f"Today: {today.strftime('%d-%m-%Y')}"
        )


    # Average traffic metrics

    avg_speed = today_traffic[
        "avg_speed"
    ].mean()

    avg_congestion = today_traffic[
        "congestion_level"
    ].mean()

    avg_vehicles = today_traffic[
        "vehicle_count"
    ].mean()

else:

    avg_speed = 0
    avg_congestion = 0
    avg_vehicles = 0

    traffic_date_label = "No traffic data"


# ============================================================
# TODAY'S AQI PREDICTION
# ============================================================

predicted_aqi = predict_aqi(today)


# ============================================================
# KPI DASHBOARD
# ============================================================

st.subheader("📊 City Status")

col1, col2, col3, col4 = st.columns(4)


# Traffic speed

col1.metric(
    "🚗 Avg Traffic Speed",
    f"{avg_speed:.1f} km/h"
)


# Congestion

col2.metric(
    "🚦 Avg Congestion",
    f"{avg_congestion:.1f}%"
)


# AQI

if predicted_aqi is not None:

    col3.metric(
        "🌫️ Predicted AQI",
        f"{predicted_aqi:.0f}"
    )

else:

    col3.metric(
        "🌫️ Predicted AQI",
        "N/A"
    )


# Vehicles

col4.metric(
    "🚙 Avg Vehicles",
    f"{avg_vehicles:,.0f}"
)


st.caption(
    f"{traffic_date_label} | "
    f"AQI prediction for {today.strftime('%d-%m-%Y')}"
)


# ============================================================
# AQI CATEGORY
# ============================================================

if predicted_aqi is not None:

    if predicted_aqi <= 50:
        aqi_category = "Good"

    elif predicted_aqi <= 100:
        aqi_category = "Satisfactory"

    elif predicted_aqi <= 200:
        aqi_category = "Moderate"

    elif predicted_aqi <= 300:
        aqi_category = "Poor"

    elif predicted_aqi <= 400:
        aqi_category = "Very Poor"

    else:
        aqi_category = "Severe"

    st.info(
        f"🌫️ Predicted AQI: **{predicted_aqi:.0f}** "
        f"— **{aqi_category}**"
    )


st.divider()

# ============================================================
# AI ASSISTANT
# ============================================================

st.divider()

st.subheader("🤖 AI Assistant")

question = st.text_input(
    "Ask about city traffic, AQI or complaints",
    placeholder="e.g. What is the traffic in Andheri today?"
)

if st.button("Ask AI"):

    if question.strip():

        # User message
        st.chat_message("user").markdown(question)

        try:

            # Run agent
            response = agent.run_agent(question)

            # =================================================
            # EXTRACT FRIENDLY ANSWER
            # =================================================

            if isinstance(response, dict):

                if response.get("success"):

                    answer = response.get(
                        "answer",
                        "Request completed successfully."
                    )

                else:

                    answer = response.get(
                        "answer",
                        response.get(
                            "error",
                            "Sorry, I could not process your request."
                        )
                    )

            else:

                answer = str(response)

            # =================================================
            # SHOW ONLY FRIENDLY ANSWER
            # =================================================

            st.chat_message(
                "assistant"
            ).markdown(answer)

        except Exception as e:

            st.error(
                f"AI Assistant Error: {e}"
            )

    else:

        st.warning(
            "Please enter a question."
        )