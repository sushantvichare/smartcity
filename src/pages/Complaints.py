
import streamlit as st
import plotly.express as px
import pandas as pd


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Citizen Complaints",
    page_icon="📢",
    layout="wide"
)

st.title("📢 Citizen Complaints Dashboard")



# ============================================================
# LOAD DATA
# ============================================================

FILE_PATH = r"G:/My Drive/Data Science/smartcity/data/complaints/bmc_complaints.csv"

df = pd.read_csv(FILE_PATH)


# ============================================================
# BASIC CLEANING
# ============================================================

# Remove completely empty columns
df = df.dropna(axis=1, how="all")

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Remove leading/trailing spaces from string columns
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype(str).str.strip()



filtered_df = df.copy()


# ============================================================
# IDENTIFY COMMON COLUMNS
# ============================================================

def find_column(possible_names):

    for name in possible_names:

        for col in df.columns:

            if col.lower().replace(" ", "_") == name:
                return col

    return None


category_col = find_column([
    "category",
    "complaint_category",
    "type",
    "complaint_type"
])

status_col = find_column([
    "status",
    "complaint_status",
    "state"
])

date_col = find_column([
    "date",
    "complaint_date",
    "created_date",
    "created_at",
    "registration_date"
])

latitude_col = find_column([
    "latitude",
    "lat"
])

longitude_col = find_column([
    "longitude",
    "lon",
    "lng"
])


# ============================================================
# KPI SECTION
# ============================================================



col1, col2, col3, col4 = st.columns(4)


# Total complaints
total_complaints = len(filtered_df)


# Status-based KPIs
if status_col:

    status_values = (
        filtered_df[status_col]
        .astype(str)
        .str.lower()
    )

    open_count = status_values.str.contains(
        "open"
    ).sum()

    resolved_count = status_values.str.contains(
        "resolved|closed|complete"
    ).sum()

    pending_count = status_values.str.contains(
        "pending"
    ).sum()

else:

    open_count = 0
    resolved_count = 0
    pending_count = 0


col1.metric(
    "Total Complaints",
    f"{total_complaints:,}"
)

col2.metric(
    "Open",
    f"{open_count:,}"
)

col3.metric(
    "Resolved",
    f"{resolved_count:,}"
)

col4.metric(
    "Pending",
    f"{pending_count:,}"
)


# ============================================================
# COMPLAINT CATEGORY DISTRIBUTION
# ============================================================

if category_col:

    st.subheader("📊 Complaints by Category")

    category_data = (
        filtered_df[category_col]
        .value_counts()
        .reset_index()
    )

    category_data.columns = [
        "Category",
        "Count"
    ]

    fig = px.pie(
        category_data,
        names="Category",
        values="Count",
        hole=0.4,
        title="Complaint Distribution by Category"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# TOP COMPLAINT CATEGORIES
# ============================================================

if category_col:

    st.subheader("🏆 Top Complaint Categories")

    top_categories = (
        filtered_df[category_col]
        .value_counts()
        .head(10)
        .sort_values()
        .reset_index()
    )

    top_categories.columns = [
        "Category",
        "Count"
    ]

    fig = px.bar(
        top_categories,
        x="Count",
        y="Category",
        orientation="h",
        text="Count",
        title="Top 10 Complaint Categories"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# COMPLAINT STATUS DISTRIBUTION
# ============================================================

if status_col:

    st.subheader("🚦 Complaint Status")

    status_data = (
        filtered_df[status_col]
        .value_counts()
        .reset_index()
    )

    status_data.columns = [
        "Status",
        "Count"
    ]

    fig = px.bar(
        status_data,
        x="Status",
        y="Count",
        color="Status",
        text="Count",
        title="Complaint Status Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# DATE-WISE COMPLAINT TREND
# ============================================================

if date_col:

    st.subheader("📅 Complaint Trend Over Time")

    filtered_df[date_col] = pd.to_datetime(
        filtered_df[date_col],
        errors="coerce"
    )

    daily_complaints = (
        filtered_df
        .dropna(subset=[date_col])
        .groupby(
            filtered_df[date_col].dt.date
        )
        .size()
        .reset_index(name="Complaints")
    )

    daily_complaints.columns = [
        "Date",
        "Complaints"
    ]

    fig = px.line(
        daily_complaints,
        x="Date",
        y="Complaints",
        markers=True,
        title="Number of Complaints Over Time"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# MONTH-WISE COMPLAINT TREND
# ============================================================

if date_col:

    st.subheader("📆 Monthly Complaint Trend")

    monthly_complaints = (
        filtered_df
        .dropna(subset=[date_col])
        .assign(
            Month=filtered_df[date_col].dt.to_period("M").astype(str)
        )
        .groupby("Month")
        .size()
        .reset_index(name="Complaints")
    )

    fig = px.bar(
        monthly_complaints,
        x="Month",
        y="Complaints",
        text="Complaints",
        title="Monthly Complaint Volume"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CATEGORY vs STATUS
# ============================================================

if category_col and status_col:

    st.subheader("🔄 Category vs Complaint Status")

    category_status = pd.crosstab(
        filtered_df[category_col],
        filtered_df[status_col]
    )

    fig = px.imshow(
        category_status,
        text_auto=True,
        aspect="auto",
        title="Complaint Category vs Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


