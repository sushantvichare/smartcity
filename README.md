# 🏙️ Smart City Intelligence Platform

### AI-Powered Urban Decision Support System for Mumbai

An end-to-end **Data Science, Machine Learning, and Generative AI platform** designed to help monitor and predict key urban conditions such as **traffic congestion, air quality, and citizen satisfaction**.

The platform combines machine learning models, historical city data, a RAG-based knowledge system, and an AI assistant into a unified **Streamlit dashboard**.

---

## 🚀 Project Overview

Modern cities generate huge amounts of data from traffic systems, environmental sensors, and citizen services.

However, this data is often isolated across different systems, making it difficult for city administrators to quickly understand what is happening and take proactive decisions.

The **Smart City Intelligence Platform** brings these capabilities together into one application.

### The platform can:

- 🚦 Monitor and predict traffic congestion
- 🌫️ Predict Air Quality Index (AQI)
- 📢 Predict citizen satisfaction
- 🤖 Answer natural-language questions using an AI assistant
- 📚 Retrieve information from a Smart City knowledge base
- 📊 Display city KPIs and analytics
- 🔎 Provide data-driven insights for urban decision making

---

# ✨ Key Features

## 🏠 Unified Dashboard

The Home dashboard provides a quick overview of the city's current status.

### KPIs

- Average traffic speed
- Average traffic congestion
- Average vehicle count
- Predicted AQI
- AQI category

The dashboard also includes an integrated AI Assistant.

---

## 🚦 Traffic Intelligence

The Traffic module analyzes historical Mumbai traffic data.

### Capabilities

- Traffic volume analysis
- Average speed analysis
- Congestion analysis
- Time-based traffic patterns
- Area-based analysis
- Traffic congestion prediction

### Example AI Query

```text
What is the traffic condition in Andheri today?
```

### AI Architecture

                         User Query
                             │
                             ▼
                    ┌─────────────────┐
                    │  Smart City AI  │
                    │    Assistant    │
                    └────────┬────────┘
                             │
                             ▼
                       Query Router
                             │
             ┌───────────────┼───────────────┐
             │               │               │
             ▼               ▼               ▼
         Traffic           AQI          Complaints
             │               │               │
             ▼               ▼               ▼
        ML Model         ML Model        ML Model
             │               │               │
             └───────────────┼───────────────┘
                             │
                             ▼
                       Response Formatter
                             │
                             ▼
                      Friendly AI Response

### Stack

| Category            | Technologies             |
| ------------------- | ------------------------ |
| Programming         | Python                   |
| Data Processing     | Pandas, NumPy            |
| Machine Learning    | Scikit-learn             |
| ML Models           | Random Forest            |
| AI / LLM            | LLM-based AI Assistant   |
| RAG                 | Vector Store + Retrieval |
| Dashboard           | Streamlit                |
| Visualization       | Plotly                   |
| Model Serialization | Joblib                   |
| Data Storage        | CSV                      |
| Version Control     | Git / GitHub             |

### 💻 Running the Project

1. git clone https://github.com/sushantvichare/smartcity.git

2. pip install -r requirements.txt

3. Add data
   data/
   ├── aqi/
   │ ├── air_quality_historical.csv
   ├── traffic/
   │ └── mumbai_traffic.csv
   └── complaints/
   └── bmc_complaints.csv

4. streamlit run src/app.py
