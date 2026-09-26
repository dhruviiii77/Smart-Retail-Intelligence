# ============================================================
# SMART RETAIL INTELLIGENCE
# AI BUSINESS INSIGHTS ENGINE
# ============================================================

import joblib
import pandas as pd


# ============================================================
# 1. LOAD TRAINED MODEL
# ============================================================

print("\nSMART RETAIL INTELLIGENCE")
print("=" * 55)
print("AI BUSINESS INSIGHTS ENGINE")
print("=" * 55)

model = joblib.load("outputs/retail_demand_model.pkl")

print("\nAI demand model loaded successfully.")


# ============================================================
# 2. DEFINE CURRENT RETAIL CONDITIONS
# ============================================================

current_conditions = pd.DataFrame([
    {
        "Hour": 18,
        "Product_Category": "Electronics",
        "Customer_Footfall": 25,
        "Discount": 10,
        "Promotion": 1
    }
])


# ============================================================
# 3. PREDICT DEMAND
# ============================================================

prediction = model.predict(current_conditions)[0]

probabilities = model.predict_proba(current_conditions)[0]

high_demand_probability = probabilities[1] * 100


# ============================================================
# 4. DISPLAY AI PREDICTION
# ============================================================

print("\nAI DEMAND PREDICTION")
print("=" * 40)

if prediction == 1:
    demand_status = "HIGH DEMAND"
else:
    demand_status = "LOW DEMAND"

print("Demand Status:", demand_status)
print(
    "High Demand Probability:",
    round(high_demand_probability, 2),
    "%"
)


# ============================================================
# 5. LOAD SALES DATA
# ============================================================

sales_df = pd.read_csv("customer_sales.csv")

print("\nSALES DATA ANALYSIS")
print("=" * 40)

total_revenue = sales_df["Revenue"].sum()
total_units = sales_df["Units_Sold"].sum()

print("Total Revenue: ₹", round(total_revenue, 2))
print("Total Units Sold:", total_units)


# ============================================================
# 6. FIND TOP REVENUE CATEGORY
# ============================================================

category_revenue = (
    sales_df
    .groupby("Product_Category")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

top_revenue_category = category_revenue.index[0]

print(
    "\nHighest Revenue Category:",
    top_revenue_category
)


# ============================================================
# 7. FIND TOP SELLING CATEGORY
# ============================================================

category_units = (
    sales_df
    .groupby("Product_Category")["Units_Sold"]
    .sum()
    .sort_values(ascending=False)
)

top_units_category = category_units.index[0]

print(
    "Best-Selling Category:",
    top_units_category
)


# ============================================================
# 8. FIND PEAK REVENUE HOUR
# ============================================================

hourly_revenue = (
    sales_df
    .groupby("Hour")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

peak_revenue_hour = hourly_revenue.index[0]

print(
    "Peak Revenue Hour:",
    peak_revenue_hour
)


# ============================================================
# 9. GENERATE AI BUSINESS RECOMMENDATIONS
# ============================================================

print("\nAI BUSINESS RECOMMENDATIONS")
print("=" * 40)

recommendations = []

if prediction == 1:
    recommendations.append(
        "Increase inventory readiness because high demand is predicted."
    )
    recommendations.append(
        "Prepare additional staff during the predicted high-demand period."
    )
else:
    recommendations.append(
        "Maintain normal inventory levels because demand is predicted to be lower."
    )

if top_revenue_category:
    recommendations.append(
        f"Prioritize {top_revenue_category} because it generates the highest revenue."
    )

if top_units_category:
    recommendations.append(
        f"Monitor {top_units_category} inventory because it has the highest unit sales."
    )

recommendations.append(
    f"Focus promotional planning around hour {peak_revenue_hour}, "
    "which currently generates the highest revenue."
)


for number, recommendation in enumerate(
    recommendations,
    start=1
):
    print(f"{number}. {recommendation}")


# ============================================================
# 10. SAVE AI INSIGHTS
# ============================================================

with open(
    "outputs/ai_business_insights.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write("SMART RETAIL INTELLIGENCE\n")
    file.write("=========================\n\n")

    file.write(
        f"Demand Status: {demand_status}\n"
    )

    file.write(
        f"High Demand Probability: "
        f"{high_demand_probability:.2f}%\n\n"
    )

    file.write(
        f"Total Revenue: ₹{total_revenue:.2f}\n"
    )

    file.write(
        f"Total Units Sold: {total_units}\n"
    )

    file.write(
        f"Highest Revenue Category: "
        f"{top_revenue_category}\n"
    )

    file.write(
        f"Best-Selling Category: "
        f"{top_units_category}\n"
    )

    file.write(
        f"Peak Revenue Hour: "
        f"{peak_revenue_hour}\n\n"
    )

    file.write("AI BUSINESS RECOMMENDATIONS\n")
    file.write("---------------------------\n")

    for number, recommendation in enumerate(
        recommendations,
        start=1
    ):
        file.write(
            f"{number}. {recommendation}\n"
        )


print(
    "\nAI insights saved to "
    "outputs/ai_business_insights.txt"
)