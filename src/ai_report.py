# ============================================================
# SMART RETAIL INTELLIGENCE
# CONSOLIDATED AI REPORT
# ============================================================

import pandas as pd


print("\nSMART RETAIL INTELLIGENCE")
print("=" * 55)
print("CONSOLIDATED AI REPORT")
print("=" * 55)


# ============================================================
# 1. LOAD SALES DATA
# ============================================================

sales_df = pd.read_csv("customer_sales.csv")


# ============================================================
# 2. CALCULATE BUSINESS METRICS
# ============================================================

total_revenue = sales_df["Revenue"].sum()
total_units = sales_df["Units_Sold"].sum()

category_revenue = (
    sales_df
    .groupby("Product_Category")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

category_units = (
    sales_df
    .groupby("Product_Category")["Units_Sold"]
    .sum()
    .sort_values(ascending=False)
)

hourly_revenue = (
    sales_df
    .groupby("Hour")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)


# ============================================================
# 3. IDENTIFY KEY BUSINESS METRICS
# ============================================================

top_revenue_category = category_revenue.index[0]
top_units_category = category_units.index[0]
peak_revenue_hour = hourly_revenue.index[0]

top_revenue = category_revenue.iloc[0]
top_units = category_units.iloc[0]
peak_hour_revenue = hourly_revenue.iloc[0]


# ============================================================
# 4. CREATE REPORT
# ============================================================

report = pd.DataFrame([
    {
        "Metric": "Total Revenue",
        "Value": total_revenue
    },
    {
        "Metric": "Total Units Sold",
        "Value": total_units
    },
    {
        "Metric": "Highest Revenue Category",
        "Value": top_revenue_category
    },
    {
        "Metric": "Highest Revenue",
        "Value": top_revenue
    },
    {
        "Metric": "Best-Selling Category",
        "Value": top_units_category
    },
    {
        "Metric": "Highest Units Sold",
        "Value": top_units
    },
    {
        "Metric": "Peak Revenue Hour",
        "Value": peak_revenue_hour
    },
    {
        "Metric": "Peak Hour Revenue",
        "Value": peak_hour_revenue
    }
])


# ============================================================
# 5. DISPLAY REPORT
# ============================================================

print("\nKEY BUSINESS METRICS")
print("=" * 40)

print(report.to_string(index=False))


# ============================================================
# 6. SAVE REPORT
# ============================================================

report.to_csv(
    "outputs/ai_report.csv",
    index=False
)

print(
    "\nAI report saved to "
    "outputs/ai_report.csv"
)