

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Traffic Analytics",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 Traffic Analytics")


# =========================================================
# LOAD DATA
# =========================================================

FILE_PATH = r"G:/My Drive/Data Science/smartcity/data/traffic/mumbai_traffic_cleaned.csv"

df = pd.read_csv(FILE_PATH)




# =========================================================
# DATA CLEANING
# =========================================================

df.columns = df.columns.str.strip()

# Display available columns
# st.write(df.columns.tolist())


# Convert possible date column
date_columns = [
    "date",
    "traffic_date",
    "timestamp",
    "datetime"
]

date_col = next(
    (col for col in date_columns if col in df.columns),
    None
)

if date_col:
    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )


# =========================================================
# COLUMN DETECTION
# =========================================================

def find_column(possible_columns):

    for col in possible_columns:

        if col in df.columns:
            return col

    return None




area_col = find_column([
    "area",
    "ward_area",
    "location",
    "zone"
])

speed_col = find_column([
    "speed",
    "average_speed",
    "avg_speed",
    "speed_kmph"
])

vehicle_col = find_column([
    "vehicles",
    "vehicle_count",
    "traffic_volume",
    "vehicle_volume",
    "num_vehicles"
])

congestion_col = find_column([
    "congestion",
    "congestion_level",
    "congestion_percentage"
])

incident_col = find_column([
    "incidents",
    "incident_count",
    "traffic_incidents"
])

hour_col = find_column([
    "hour",
    "hour_of_day"
])

day_col = find_column([
    "day",
    "day_of_week"
])



filtered_df = df.copy()

filtered_df["datetime"] = pd.to_datetime(
    filtered_df["datetime"],
    errors="coerce"
)

filtered_df["hour"] = filtered_df["datetime"].dt.hour




# =========================================================
# KPIs
# =========================================================

col1, col2, col3, col4 = st.columns(4)


# Average Speed

if speed_col:

    avg_speed = (
        pd.to_numeric(
            filtered_df[speed_col],
            errors="coerce"
        )
        .mean()
    )

    col1.metric(
        "Average Speed",
        f"{avg_speed:.1f} km/h"
    )

else:

    col1.metric(
        "Average Speed",
        "N/A"
    )


# Average Congestion

if congestion_col:

    avg_congestion = (
        pd.to_numeric(
            filtered_df[congestion_col],
            errors="coerce"
        )
        .mean()
    )

    col2.metric(
        "Avg Congestion",
        f"{avg_congestion:.1f}%"
    )

else:

    col2.metric(
        "Avg Congestion",
        "N/A"
    )


# Vehicles

if vehicle_col:

    total_vehicles = (
        pd.to_numeric(
            filtered_df[vehicle_col],
            errors="coerce"
        )
        .sum()
    )

    col3.metric(
        "Vehicles",
        f"{total_vehicles:,.0f}"
    )

else:

    col3.metric(
        "Vehicles",
        "N/A"
    )


# Incidents

if incident_col:

    total_incidents = (
        pd.to_numeric(
            filtered_df[incident_col],
            errors="coerce"
        )
        .sum()
    )

    col4.metric(
        "Incidents",
        f"{total_incidents:,.0f}"
    )

else:

    col4.metric(
        "Incidents",
        "N/A"
    )


st.divider()


# =========================================================
# TRAFFIC VOLUME BY HOUR
# =========================================================

st.subheader("📊 Traffic Volume by Hour")

if hour_col and vehicle_col:

    hourly_traffic = (
        filtered_df
        .groupby(hour_col)[vehicle_col]
        .sum()
        .reset_index()
        .sort_values(hour_col)
    )

    fig = px.line(
        hourly_traffic,
        x=hour_col,
        y=vehicle_col,
        markers=True,
        title="Vehicle Volume by Hour"
    )

    fig.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Number of Vehicles"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        "Hour or vehicle column not found."
    )


# =========================================================
# AVERAGE SPEED BY HOUR
# =========================================================

st.subheader("🏎 Average Speed by Hour")

if hour_col and speed_col:

    speed_hourly = (
        filtered_df
        .groupby(hour_col)[speed_col]
        .mean()
        .reset_index()
        .sort_values(hour_col)
    )

    fig = px.line(
        speed_hourly,
        x=hour_col,
        y=speed_col,
        markers=True,
        title="Average Speed by Hour"
    )

    fig.update_layout(
        xaxis_title="Hour",
        yaxis_title="Average Speed (km/h)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# CONGESTION BY HOUR
# =========================================================

st.subheader("🚧 Congestion by Hour")

if hour_col and congestion_col:

    congestion_hourly = (
        filtered_df
        .groupby(hour_col)[congestion_col]
        .mean()
        .reset_index()
        .sort_values(hour_col)
    )

    fig = px.bar(
        congestion_hourly,
        x=hour_col,
        y=congestion_col,
        color=congestion_col,
        title="Average Congestion by Hour"
    )

    fig.update_layout(
        xaxis_title="Hour",
        yaxis_title="Congestion (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# AREA-WISE TRAFFIC
# =========================================================

st.subheader("📍 Area-wise Traffic")

if area_col and vehicle_col:

    area_traffic = (
        filtered_df
        .groupby(area_col)[vehicle_col]
        .sum()
        .reset_index()
        .sort_values(
            vehicle_col,
            ascending=False
        )
        .head(15)
    )

    fig = px.bar(
        area_traffic,
        x=area_col,
        y=vehicle_col,
        color=vehicle_col,
        title="Top Areas by Traffic Volume"
    )

    fig.update_layout(
        xaxis_title="Area",
        yaxis_title="Vehicle Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# AREA-WISE SPEED
# =========================================================

st.subheader("🏙 Area-wise Average Speed")

if area_col and speed_col:

    area_speed = (
        filtered_df
        .groupby(area_col)[speed_col]
        .mean()
        .reset_index()
        .sort_values(speed_col)
        .head(15)
    )

    fig = px.bar(
        area_speed,
        x=speed_col,
        y=area_col,
        color=speed_col,
        orientation="h",
        title="Areas with Lowest Average Speed"
    )

    fig.update_layout(
        xaxis_title="Average Speed (km/h)",
        yaxis_title="Area"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# DAY-WISE TRAFFIC
# =========================================================

st.subheader("📅 Day-wise Traffic")

if day_col and vehicle_col:

    day_traffic = (
        filtered_df
        .groupby(day_col)[vehicle_col]
        .sum()
        .reset_index()
    )

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    day_traffic[day_col] = pd.Categorical(
        day_traffic[day_col],
        categories=day_order,
        ordered=True
    )

    day_traffic = day_traffic.sort_values(
        day_col
    )

    fig = px.bar(
        day_traffic,
        x=day_col,
        y=vehicle_col,
        color=vehicle_col,
        title="Traffic Volume by Day"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TRAFFIC HEATMAP
# =========================================================

st.subheader("🔥 Traffic Heatmap")

if day_col and hour_col and vehicle_col:

    heatmap_data = pd.pivot_table(
        filtered_df,
        values=vehicle_col,
        index=day_col,
        columns=hour_col,
        aggfunc="mean"
    )

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    heatmap_data = heatmap_data.reindex(
        [
            d for d in day_order
            if d in heatmap_data.index
        ]
    )

    fig = px.imshow(
        heatmap_data,
        aspect="auto",
        labels={
            "x": "Hour",
            "y": "Day",
            "color": "Vehicles"
        },
        title="Traffic Volume Heatmap"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# INCIDENT ANALYSIS
# =========================================================

st.subheader("⚠️ Traffic Incidents")

if incident_col:

    incident_data = (
        filtered_df
        .groupby(
            hour_col
        )[incident_col]
        .sum()
        .reset_index()
        if hour_col
        else None
    )

    if incident_data is not None:

        fig = px.bar(
            incident_data,
            x=hour_col,
            y=incident_col,
            color=incident_col,
            title="Traffic Incidents by Hour"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# SPEED VS VEHICLE VOLUME
# =========================================================

st.subheader("📈 Speed vs Traffic Volume")

if speed_col and vehicle_col:

    scatter_df = filtered_df[
        [speed_col, vehicle_col]
    ].copy()

    scatter_df = scatter_df.dropna()

    fig = px.scatter(
        scatter_df,
        x=vehicle_col,
        y=speed_col,
        trendline="ols",
        title="Relationship Between Vehicle Volume and Speed"
    )

    fig.update_layout(
        xaxis_title="Vehicle Volume",
        yaxis_title="Average Speed (km/h)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# CONGESTION LEVEL
# =========================================================

st.subheader("🚦 Congestion Level Distribution")

if congestion_col:

    congestion_values = pd.to_numeric(
        filtered_df[congestion_col],
        errors="coerce"
    )

    congestion_category = pd.cut(
        congestion_values,
        bins=[
            -np.inf,
            30,
            60,
            80,
            np.inf
        ],
        labels=[
            "Low",
            "Moderate",
            "High",
            "Severe"
        ]
    )

    congestion_counts = (
        congestion_category
        .value_counts()
        .reindex(
            [
                "Low",
                "Moderate",
                "High",
                "Severe"
            ]
        )
        .fillna(0)
        .reset_index()
    )

    congestion_counts.columns = [
        "Congestion Level",
        "Count"
    ]

    fig = px.pie(
        congestion_counts,
        names="Congestion Level",
        values="Count",
        title="Congestion Level Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# PEAK HOUR ANALYSIS
# =========================================================

st.subheader("⏰ Peak Traffic Analysis")

if hour_col and vehicle_col:

    peak_hour = (
        filtered_df
        .groupby(hour_col)[vehicle_col]
        .mean()
        .idxmax()
    )

    peak_volume = (
        filtered_df
        .groupby(hour_col)[vehicle_col]
        .mean()
        .max()
    )

    st.info(
        f"Peak traffic occurs around "
        f"{int(peak_hour):02d}:00 with approximately "
        f"{peak_volume:,.0f} vehicles."
    )


# =========================================================
# CONGESTION PREDICTION
# =========================================================

st.subheader("🤖 Traffic Prediction")

if hour_col and vehicle_col:

    hourly_volume = (
        filtered_df
        .groupby(hour_col)[vehicle_col]
        .mean()
    )

    if len(hourly_volume) > 0:

        peak_hour = hourly_volume.idxmax()

        if 17 <= peak_hour <= 20:

            prediction = (
                "High congestion is expected during "
                "the evening peak period."
            )

        elif 7 <= peak_hour <= 10:

            prediction = (
                "High congestion is expected during "
                "the morning peak period."
            )

        else:

            prediction = (
                f"Peak traffic is currently around "
                f"{int(peak_hour):02d}:00."
            )

        st.success(prediction)



