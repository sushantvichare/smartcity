history = pd.read_csv(FILE_PATH)

history["date"] = pd.to_datetime(
    history["date"],
    format="%d-%m-%Y",
    errors="coerce"
)

history = history[["date", "us_aqi"]].dropna()



target_date = "2026-02-20"

predicted_aqi = predict_aqi(
    target_date,
    history
)

print()
print("=" * 50)
print("AQI PREDICTION")
print("=" * 50)

print(f"Date          : {target_date}")
print(f"Predicted AQI : {predicted_aqi}")
