# train_citizen_satisfaction_model.py

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ===========================
# Load Dataset
# ===========================
df = pd.read_csv(r"G:\My Drive\Data Science\smartcity\data\complaints\bmc_complaints.csv")

print(df.head())
print(df.columns)

# =====================================================
# CHANGE THIS TO YOUR TARGET COLUMN NAME
# =====================================================
TARGET = "citizen_satisfied"

# Drop rows with missing target
df = df.dropna(subset=[TARGET])

# ===========================
# Date Feature Engineering
# ===========================
date_cols = df.select_dtypes(include="object").columns

for col in date_cols:
    try:
        temp = pd.to_datetime(df[col])
        if temp.notna().sum() > len(df) * 0.5:
            df[col + "_year"] = temp.dt.year
            df[col + "_month"] = temp.dt.month
            df[col + "_day"] = temp.dt.day
            df.drop(columns=col, inplace=True)
    except:
        pass

# ===========================
# Features & Target
# ===========================
X = df.drop(columns=[TARGET])
y = df[TARGET]

# ===========================
# Detect Feature Types
# ===========================
categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()

numeric_cols = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

# ===========================
# Preprocessing
# ===========================
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols)
    ]
)

# ===========================
# Model
# ===========================
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    max_depth=15
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])

# ===========================
# Train Test Split
# ===========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ===========================
# Train
# ===========================
pipeline.fit(X_train, y_train)

# ===========================
# Evaluate
# ===========================
pred = pipeline.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, pred))
print("\nClassification Report\n")
print(classification_report(y_test, pred))

# ===========================
# Save Model
# ===========================
joblib.dump(pipeline, "models/citizen_satisfaction_model.pkl")

print("\nModel saved as citizen_satisfaction_model.pkl")