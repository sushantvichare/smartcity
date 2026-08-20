
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import ibis


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Air Quality",
    page_icon="🌫",
    layout="wide"
)

st.title("🌫 Air Quality")



# --------------------------------------------------
# LOAD DATA USING IBIS
# --------------------------------------------------
con = ibis.duckdb.connect()

df_ibis = con.read_csv(
    r"G:/My Drive/Data Science/smartcity/data/aqi/aqi_cleaned.csv"
)

# Convert Ibis table to Pandas
df = df_ibis.execute()


# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

# Convert date column if available
if "date" in df.columns:
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

# Convert numeric columns
numeric_columns = [
    "us_aqi",
    "pm2_5",
    "pm10",
    "co",
    "no2",
    "so2",
    "o3"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


filtered_df = df.copy()


# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------



col1, col2, col3, col4 = st.columns(4)


avg_aqi = filtered_df["us_aqi"].mean()

avg_pm25 = (
    filtered_df["pm2_5"].mean()
    if "pm2_5" in filtered_df.columns
    else 0
)

avg_pm10 = (
    filtered_df["pm10"].mean()
    if "pm10" in filtered_df.columns
    else 0
)

max_aqi = filtered_df["us_aqi"].max()


col1.metric(
    "Average AQI",
    f"{avg_aqi:.2f}"
)

col2.metric(
    "Average PM2.5",
    f"{avg_pm25:.2f} µg/m³"
)

col3.metric(
    "Average PM10",
    f"{avg_pm10:.2f} µg/m³"
)

col4.metric(
    "Maximum AQI",
    f"{max_aqi:.0f}"
)



# --------------------------------------------------
# EDA - AQI DISTRIBUTION
# --------------------------------------------------

st.subheader("📈 AQI Distribution")

fig = px.histogram(
    filtered_df,
    x="us_aqi",
    nbins=30,
    marginal="box",
    title="Distribution of US AQI",
    labels={
        "us_aqi": "AQI"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# AQI OVER TIME
# --------------------------------------------------

if "date" in filtered_df.columns:

    st.subheader("📅 AQI Trend Over Time")

    daily_aqi = (
        filtered_df
        .dropna(subset=["date"])
        .groupby("date", as_index=False)["us_aqi"]
        .mean()
    )

    fig = px.line(
        daily_aqi,
        x="date",
        y="us_aqi",
        markers=True,
        title="Average AQI Over Time",
        labels={
            "date": "Date",
            "us_aqi": "Average AQI"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# POLLUTANT DISTRIBUTIONS
# --------------------------------------------------

st.subheader("🧪 Pollutant Distributions")

pollutants = [
    col for col in [
        "pm2_5",
        "pm10",
        "co",
        "no2",
        "so2",
        "o3"
    ]
    if col in filtered_df.columns
]

if pollutants:

    selected_pollutant = st.selectbox(
        "Select Pollutant",
        pollutants
    )

    fig = px.histogram(
        filtered_df,
        x=selected_pollutant,
        nbins=30,
        marginal="box",
        title=f"{selected_pollutant.upper()} Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# AREA-WISE AQI
# --------------------------------------------------

if "area" in filtered_df.columns:

    st.subheader("📍 Area-wise AQI")

    area_aqi = (
        filtered_df
        .groupby("area", as_index=False)["us_aqi"]
        .mean()
        .sort_values(
            "us_aqi",
            ascending=False
        )
    )

    fig = px.bar(
        area_aqi,
        x="area",
        y="us_aqi",
        color="us_aqi",
        title="Average AQI by Area",
        labels={
            "area": "Area",
            "us_aqi": "Average AQI"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# AQI CATEGORY
# --------------------------------------------------

st.subheader("🚦 AQI Category Distribution")


def aqi_category(aqi):

    if pd.isna(aqi):
        return "Unknown"

    if aqi <= 50:
        return "Good"

    elif aqi <= 100:
        return "Moderate"

    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"

    elif aqi <= 200:
        return "Unhealthy"

    elif aqi <= 300:
        return "Very Unhealthy"

    else:
        return "Hazardous"


filtered_df["AQI_Category"] = (
    filtered_df["us_aqi"]
    .apply(aqi_category)
)

category_counts = (
    filtered_df["AQI_Category"]
    .value_counts()
    .reset_index()
)

category_counts.columns = [
    "AQI_Category",
    "Count"
]

fig = px.pie(
    category_counts,
    names="AQI_Category",
    values="Count",
    hole=0.4,
    title="AQI Category Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# POLLUTANT vs AQI
# --------------------------------------------------

st.subheader("🔬 Pollutants vs AQI")

if pollutants:

    selected_pollutant_2 = st.selectbox(
        "Select pollutant for relationship analysis",
        pollutants,
        key="pollutant_relationship"
    )

    fig = px.scatter(
        filtered_df,
        x=selected_pollutant_2,
        y="us_aqi",
        trendline="ols",
        title=f"{selected_pollutant_2.upper()} vs AQI",
        opacity=0.6
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# CORRELATION HEATMAP
# --------------------------------------------------

st.subheader("🔥 Correlation Heatmap")

correlation_columns = [
    col for col in [
        "us_aqi",
        "pm2_5",
        "pm10",
        "co",
        "no2",
        "so2",
        "o3"
    ]
    if col in filtered_df.columns
]

if len(correlation_columns) >= 2:

    corr = filtered_df[
        correlation_columns
    ].corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        title="AQI & Pollutant Correlation Matrix"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# GEOGRAPHICAL MAP
# --------------------------------------------------

if (
    "latitude" in filtered_df.columns
    and
    "longitude" in filtered_df.columns
):

    st.subheader("🗺 AQI Monitoring Locations")

    map_df = filtered_df[
        [
            "latitude",
            "longitude",
            "us_aqi"
        ]
    ].dropna()

    st.map(
        map_df,
        latitude="latitude",
        longitude="longitude"
    )


# --------------------------------------------------
# TOP POLLUTED AREAS
# --------------------------------------------------

if "area" in filtered_df.columns:

    st.subheader("🚨 Top 10 Most Polluted Areas")

    top_areas = (
        filtered_df
        .groupby("area")["us_aqi"]
        .mean()
        .sort_values(
            ascending=False
        )
        .head(10)
        .reset_index()
    )

    top_areas.columns = [
        "Area",
        "Average AQI"
    ]

    st.dataframe(
        top_areas,
        use_container_width=True
    )


