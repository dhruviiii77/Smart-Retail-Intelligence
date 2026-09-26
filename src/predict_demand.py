# ============================================================
# SMART RETAIL INTELLIGENCE
# INTERACTIVE RETAIL DEMAND PREDICTION SYSTEM
# ============================================================

import joblib
import pandas as pd


# ============================================================
# 1. LOAD TRAINED MODEL
# ============================================================

print("\nSMART RETAIL INTELLIGENCE")
print("=" * 55)
print("INTERACTIVE RETAIL DEMAND PREDICTION SYSTEM")
print("=" * 55)

model = joblib.load("outputs/retail_demand_model.pkl")

print("\nTrained model loaded successfully.")


# ============================================================
# 2. GET INPUT FROM USER
# ============================================================

print("\nENTER RETAIL CONDITIONS")
print("=" * 40)

hour = int(input("Enter hour (10-19): "))

category = input(
    "Enter product category (Electronics/Clothing/Grocery): "
)

footfall = int(
    input("Enter expected customer footfall: ")
)

discount = int(
    input("Enter discount percentage: ")
)

promotion = int(
    input("Is there a promotion? (1 = Yes, 0 = No): ")
)


# ============================================================
# 3. CREATE INPUT DATAFRAME
# ============================================================

new_data = pd.DataFrame([
    {
        "Hour": hour,
        "Product_Category": category,
        "Customer_Footfall": footfall,
        "Discount": discount,
        "Promotion": promotion
    }
])


# ============================================================
# 4. DISPLAY INPUT
# ============================================================

print("\nRETAIL CONDITIONS")
print("=" * 40)

print("Hour:", hour)
print("Product Category:", category)
print("Customer Footfall:", footfall)
print("Discount:", discount, "%")
print("Promotion:", "Yes" if promotion == 1 else "No")


# ============================================================
# 5. MAKE PREDICTION
# ============================================================

prediction = model.predict(new_data)[0]


# ============================================================
# 6. GET PREDICTION PROBABILITY
# ============================================================

probabilities = model.predict_proba(new_data)[0]

low_demand_probability = probabilities[0] * 100
high_demand_probability = probabilities[1] * 100


# ============================================================
# 7. DISPLAY RESULT
# ============================================================

print("\nDEMAND PREDICTION")
print("=" * 40)

if prediction == 1:

    print("Predicted Demand: HIGH DEMAND")
    print(
        "High Demand Probability:",
        round(high_demand_probability, 2),
        "%"
    )

else:

    print("Predicted Demand: LOW DEMAND")
    print(
        "Low Demand Probability:",
        round(low_demand_probability, 2),
        "%"
    )


# ============================================================
# 8. BUSINESS RECOMMENDATION
# ============================================================

print("\nBUSINESS RECOMMENDATION")
print("=" * 40)

if prediction == 1:

    print("• Prepare additional inventory.")
    print("• Increase staff availability.")
    print("• Maintain strong product visibility.")

else:

    print("• Maintain normal inventory levels.")
    print("• Use targeted promotions if required.")
    print("• Avoid unnecessary overstocking.")


# ============================================================
# 9. FINAL MESSAGE
# ============================================================

print("\nPrediction completed successfully.")