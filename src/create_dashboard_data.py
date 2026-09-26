from pathlib import Path
import pandas as pd
import joblib

print("\nSMART RETAIL INTELLIGENCE - DASHBOARD DATA")
print("=" * 55)

# Project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# File paths
data_path = BASE_DIR / "ml_training_data.csv"
model_path = BASE_DIR / "outputs" / "retail_demand_model.pkl"
output_path = BASE_DIR / "dashboard_data.csv"

# Load training data
df = pd.read_csv(data_path)

print("\nTraining data loaded successfully.")
print("Rows:", len(df))

# Load trained ML model
model = joblib.load(model_path)

print("ML model loaded successfully.")

# Features used by the ML model
features = [
    "Hour",
    "Product_Category",
    "Customer_Footfall",
    "Discount",
    "Promotion"
]

# Prepare data for prediction
X = df[features]

# Generate predictions
predictions = model.predict(X)

# Probability of High Demand
probabilities = model.predict_proba(X)[:, 1]

# Create dashboard data
dashboard_df = df[
    [
        "Date",
        "Hour",
        "Product_Category",
        "Units_Sold",
        "Revenue",
        "Customer_Footfall",
        "Discount",
        "Promotion"
    ]
].copy()

# Add High Demand prediction
dashboard_df["High_Demand"] = [
    "High Demand" if prediction == 1 else "Low Demand"
    for prediction in predictions
]

# Add prediction probability
dashboard_df["Prediction_Probability"] = (
    probabilities * 100
).round(2)

# Save dashboard data
dashboard_df.to_csv(output_path, index=False)

print("\nDashboard data created successfully!")
print("Saved to:", output_path)

print("\nDataset shape:")
print(dashboard_df.shape)

print("\nColumns:")
print(dashboard_df.columns.tolist())

print("\nFirst 5 rows:")
print(dashboard_df.head())

print("\nDONE!")