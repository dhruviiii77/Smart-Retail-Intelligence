# ============================================================
# SMART RETAIL INTELLIGENCE
# MACHINE LEARNING MODEL
# ============================================================

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# 1. LOAD TRAINING DATA
# ============================================================

print("\nSMART RETAIL INTELLIGENCE - MACHINE LEARNING")
print("=" * 55)

df = pd.read_csv("ml_training_data.csv")

print("\nDataset loaded successfully.")
print("Dataset shape:", df.shape)

print("\nDataset preview:")
print(df.head())


# ============================================================
# 2. CHECK DATA QUALITY
# ============================================================

print("\nDATA QUALITY CHECK")
print("=" * 40)

print("\nMissing values:")
print(df.isnull().sum())

print("\nData types:")
print(df.dtypes)


# ============================================================
# 3. CREATE MACHINE LEARNING TARGET
# ============================================================

# We want the model to predict whether demand is HIGH or LOW.
#
# We use Units_Sold only to create the target.
# Units_Sold itself will NOT be used as a model feature.
#
# This prevents target leakage.

demand_threshold = df["Units_Sold"].median()

df["High_Demand"] = (
    df["Units_Sold"] >= demand_threshold
).astype(int)

print("\nDEMAND TARGET")
print("=" * 40)

print("Demand threshold:", demand_threshold)

print("\nTarget distribution:")
print(df["High_Demand"].value_counts())

print("\n0 = Low Demand")
print("1 = High Demand")


# ============================================================
# 4. SELECT FEATURES
# ============================================================

features = [
    "Hour",
    "Product_Category",
    "Customer_Footfall",
    "Discount",
    "Promotion"
]

target = "High_Demand"

X = df[features]
y = df[target]

print("\nFEATURES USED BY MODEL")
print("=" * 40)

for feature in features:
    print("-", feature)

print("\nFeature matrix shape:", X.shape)
print("Target shape:", y.shape)


# ============================================================
# 5. TRAIN-TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTRAIN-TEST SPLIT")
print("=" * 40)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 6. PREPROCESS CATEGORICAL DATA
# ============================================================

categorical_features = [
    "Product_Category"
]

numeric_features = [
    "Hour",
    "Customer_Footfall",
    "Discount",
    "Promotion"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "category",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# ============================================================
# 7. CREATE RANDOM FOREST MODEL
# ============================================================

random_forest = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


# ============================================================
# 8. CREATE COMPLETE ML PIPELINE
# ============================================================

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", random_forest)
    ]
)


# ============================================================
# 9. TRAIN MODEL
# ============================================================

print("\nTRAINING RANDOM FOREST")
print("=" * 40)

model.fit(X_train, y_train)

print("Model trained successfully.")


# ============================================================
# 10. GENERATE PREDICTIONS
# ============================================================

y_pred = model.predict(X_test)

print("\nMODEL PREDICTIONS")
print("=" * 40)

print("Actual values:")
print(y_test.tolist())

print("\nPredicted values:")
print(y_pred.tolist())


# ============================================================
# 11. MODEL EVALUATION
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

print("\nMODEL EVALUATION")
print("=" * 40)

print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Low Demand", "High Demand"],
        zero_division=0
    )
)


# ============================================================
# 12. BUSINESS INTERPRETATION
# ============================================================

print("\nBUSINESS INTERPRETATION")
print("=" * 40)

print(
    "The model predicts whether a retail situation is likely "
    "to generate high customer demand."
)

print(
    "It uses customer footfall, time, product category, "
    "discount and promotion information."
)

print(
    "\nThis can help retailers plan inventory, promotions "
    "and staffing decisions."
)

# ============================================================
# 13. SAVE TRAINED MODEL
# ============================================================

import joblib

print("\nSAVING TRAINED MODEL")
print("=" * 40)

joblib.dump(model, "outputs/retail_demand_model.pkl")

print("Trained model saved successfully.")
print("Location: outputs/retail_demand_model.pkl")

# 14. CONFUSION MATRIX

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

print("\nCONFUSION MATRIX")
print("=" * 40)

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

plt.figure(figsize=(7, 5))

plt.imshow(cm)

plt.title("Retail Demand Prediction - Confusion Matrix")
plt.xlabel("Predict Demad")
plt.ylabel("Actual Demand")

plt.xticks(
    [0,1],
    ["Low Demand", "High Demand"]
)

plt.yticks(
    [0,1],
    ["Low Demand", "High Deamnd"]
)

for i in range(2):
    for j in range(2):
        plt.text(
            j,
            i,
            cm[i, j],
            ha="center",
            va="center"
        )

plt.tight_layout()

plt.savefig(
    "outputs/demand_confusion_matrix.png"
)
plt.show()

print(
    "\nConfusion matrix saved to "
    "outputs/demand_confusion_matrix.png"
)

# 15. FEATURE IMPORTANCE ANALYSIS

print("\nFEATURE IMPORTANCE ANALYSIS")
print("=" * 40)

# Get feature names after one-hot encoding
feature_names = (
    model.named_steps["preprocessor"]
    .get_feature_names_out()
)

# Get importance values from Random Forest
importance_values = (
    model.named_steps["classifier"]
    .feature_importances_
)

feature_importance = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance_values
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)
print("\nFeature Importance Ranking:")

for feature, importance in zip(
    feature_importance["Feature"],
    feature_importance["Importance"]
):
    print(
        feature,
        ":",
        round(importance, 4)
    )

# 16. FEATURE IMPORTANCE CHART

plt.figure(figsize=(9, 6))

plt.barh(
    feature_importance["Feature"],
    feature_importance["Importance"]
)

plt.title("Retail Demand Prediction - Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Feature")

plt.tight_layout()

plt.savefig(
    "outputs/demand_feature_importance.png"
)
plt.show()

print(
    "\nFeature importance chart saved to "
    "outputs/demand_feature_importance.png"
)

# 17. EXPORT FEATURE IMPORTANCE

feature_importance.to_csv(
    "outputs/demand_feature_importance.csv",
    index=False
)
print(
    "\nFeature importance data saved to "
    "outputs/demand_feature_importance.csv"
)