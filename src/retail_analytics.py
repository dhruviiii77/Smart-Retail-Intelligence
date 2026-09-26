import csv
import matplotlib.pyplot as plt

sales_file = "customer_sales.csv"
customer_file = "customer_data.csv"


# 1. SALES BY PRODUCT CATEGORY

category_sales = {}

with open(sales_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        category = row["Product_Category"]
        units = int(row["Units_Sold"])

        if category not in category_sales:
            category_sales[category] = units
        else:
            category_sales[category] += units


# Find the best-selling category
best_category = max(category_sales, key=category_sales.get)


print("SMART RETAIL ANALYTICS")
print("=" * 30)

print("\nSales by Category:")

for category, units in category_sales.items():
    print(category, ":", units, "units")

print("\nBest-Selling Category:", best_category)
print("Units Sold:", category_sales[best_category])


# 2. REVENUE BY PRODUCT CATEGORY

category_revenue = {}

with open(sales_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        category = row["Product_Category"]
        revenue = float(row["Revenue"])

        if category not in category_revenue:
            category_revenue[category] = revenue
        else:
            category_revenue[category] += revenue


# Find the highest revenue category
highest_revenue_category = max(
    category_revenue,
    key=category_revenue.get
)


print("\nRevenue by Category:")

for category, revenue in category_revenue.items():
    print(category, ": ₹", revenue)

print(
    "\nHighest Revenue Category:",
    highest_revenue_category
)

print(
    "Revenue: ₹",
    category_revenue[highest_revenue_category]
)


# 3. REVENUE BY CATEGORY CHART

categories = list(category_revenue.keys())
revenues = list(category_revenue.values())

plt.figure(figsize=(8, 5))

plt.bar(categories, revenues)

plt.title("Revenue by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Revenue (₹)")

plt.tight_layout()

plt.savefig("outputs/revenue_by_category_chart.png")

plt.show()


# 4. READ CUSTOMER FOOTFALL DATA

total_entries = 0
total_exits = 0
peak_customers_inside = 0
current_customers_inside = 0

with open(customer_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:

        entered = int(row["Entered"])
        exited = int(row["Exited"])
        customers_inside = int(row["Customers Inside"])

        total_entries = max(
            total_entries,
            entered
        )

        total_exits = max(
            total_exits,
            exited
        )

        peak_customers_inside = max(
            peak_customers_inside,
            customers_inside
        )

        current_customers_inside = customers_inside

print("Total Entries:", total_entries)
print("Total Exits:", total_exits)
print("Peak Customers Inside:", peak_customers_inside)
print("Current Customers Inside:", current_customers_inside)

# 5. TOTAL REVENUE

total_revenue = sum(category_revenue.values())

print("\nTotal Customer Entries:", total_entries)

print("Total Revenue: ₹", total_revenue)

# 6. REVENUE PER CUSTOMER

revenue_per_customer = (
    total_revenue / total_entries
    if total_entries > 0
    else 0
)

print(
    "Revenue per Customer: ₹",
    round(revenue_per_customer, 2)
)

# 7. SALES BY HOUR

hourly_revenue = {}

with open(sales_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        hour = row["Hour"]
        revenue = float(row["Revenue"])

        if hour not in hourly_revenue:
            hourly_revenue[hour] = revenue
        else:
            hourly_revenue[hour] += revenue


# Find the highest revenue hour
best_sales_hour = max(
    hourly_revenue,
    key=hourly_revenue.get
)

print("\nRevenue by Hour:")

for hour, revenue in hourly_revenue.items():
    print(hour, "→ ₹", revenue)

print("\nHighest Revenue Hour:", best_sales_hour)
print(
    "Revenue During This Hour: ₹",
    hourly_revenue[best_sales_hour]
)

# 8. BUSINESS PERFORMANCE INSIGHT

print("\nBUSINESS PERFORMANCE INSIGHT")
print("=" * 30)

if best_category == highest_revenue_category:
    print(
        "The same category is leading in both units sold and revenue:"
    )
    print(best_category)
else:
    print(
        "The best-selling category by units is:",
        best_category
    )
    print(
        "The highest-revenue category is:",
        highest_revenue_category
    )

print(
    "\nThis shows that the category with the most units sold "
    "is not necessarily the category generating the most revenue."
)

# 9. REVENUE PER CUSTOMER ENTRY

if total_entries > 0:
    revenue_per_entry = total_revenue / total_entries
else:
    revenue_per_entry = 0

print("\nREVENUE PER CUSTOMER ENTRY")
print("=" * 30)

print(
    "Revenue per Customer Entry: ₹",
    round(revenue_per_entry, 2)
)

# 10. HOURLY TRAFFIC VS REVENUE

# Read customer footfall by hour
hourly_footfall = {}

with open(customer_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        timestamp = row["Timestamp"]
        hour = timestamp[11:13]

        entries = int(row["Entered"])

        if hour not in hourly_footfall:
            hourly_footfall[hour] = entries
        else:
            hourly_footfall[hour] = max(
                hourly_footfall[hour],
                entries
            )


print("\nHOURLY TRAFFIC VS REVENUE")
print("=" * 30)

for hour in hourly_revenue:

    footfall = hourly_footfall.get(hour, 0)
    revenue = hourly_revenue[hour]

    print(
        "Hour:", hour,
        "| Customers:", footfall,
        "| Revenue: ₹", revenue
    )

# 11. HOURLY CUSTOMERS VS REVENUE CHART

hours = sorted(hourly_revenue.keys())

customer_counts = [
    hourly_footfall.get(hour, 0)
    for hour in hours
]

revenue_values = [
    hourly_revenue[hour]
    for hour in hours
]

fig, ax1 = plt.subplots(figsize=(10, 5))

# Customer traffic
ax1.set_xlabel("Hour")
ax1.set_ylabel("Customers")

ax1.bar(
    hours,
    customer_counts,
    alpha=0.6,
    label="Customers"
)

# Revenue
ax2 = ax1.twinx()

ax2.set_ylabel("Revenue (₹)")

ax2.plot(
    hours,
    revenue_values,
    marker="o",
    linewidth=2,
    label="Revenue"
)

plt.title("Hourly Customer Traffic vs Revenue")

fig.tight_layout()

plt.savefig(
    "outputs/hourly_customers_vs_revenue.png"
)

plt.show()

# 12. REVENUE PER CUSTOMER BY HOUR

hourly_revenue_per_customer = {}

for hour in hourly_revenue:

    customers = hourly_footfall.get(hour, 0)
    revenue = hourly_revenue[hour]

    if customers > 0:
        hourly_value = revenue / customers
    else:
        hourly_value = 0

    hourly_revenue_per_customer[hour] = hourly_value

print("\nREVENUE PER CUSTOMER BY HOUR")
print("=" * 30)

for hour, value in hourly_revenue_per_customer.items():

    print(
        "Hour:", hour,
        "| Revenue per Customer: ₹",
        round(value, 2)
    )

# Find highest-value hour
best_value_hour = max(
    hourly_revenue_per_customer,
    key=hourly_revenue_per_customer.get
)

print(
    "\nHighest Revenue per Customer Hour:",
    best_value_hour
)

print(
    "Revenue per Customer: ₹",
    round(
        hourly_revenue_per_customer[best_value_hour],
        2
    )
)
# 13. REVENUE PER CUSTOMER BY HOUR CHART

hours= sorted(hourly_revenue_per_customer.keys())
values = [
    hourly_revenue_per_customer[hour]
    for hour in hours
]    

plt.figure(figsize=(10,5))

plt.bar(hours, values)

plt.title("Revenue per Customer by Hour")
plt.xlabel("Hour")
plt.ylabel(" Revenue per Customer (₹)")

plt.tight_layout()

plt.savefig(
    "outputs/revenue_per_customer_by_hour.png"
)
plt.show()

# 14. FINAL BUSINESS SUMMARY

report_file = "outputs/retail_business_report.txt"

with open(report_file, "w", encoding="utf-8") as file:

    file.write("SMART RETAIL INTELLIGENCE\n")
    file.write("=" * 40 + "\n")

    file.write(
        f" Total Customer Entries: {total_entries}\n"
    )
    file.write(
        f"Total Revenue: ₹{total_revenue:.2f}\n"
    )
    file.write(
        f"Revenue per Customer: ₹{revenue_per_customer:.2f}\n"
    )
    file.write(
        f"Best Selling Category: {best_category}\n"
    )
    file.write(
        f"Units Sold in Best Category: "
        f"{category_sales[best_category]}\n"
    )
    file.write(
        f"Highest Revenue Hour: {best_sales_hour}\n"
    )
    file.write(
        f"Highest Revenue per Customer Hour: "
        f"{best_value_hour}\n"
    )
    file.write("\nBUSINESS INSIGHTS\n")
    file.write("=" * 40 + "\n")
    
    file.write(
        f"{best_category} is the best selling category "
        f"based on units sold.\n"
    )

    file.write(
        f"{highest_revenue_category} generates the highest "
        f"total revenue.\n"
    )

    file.write(
        f"Hour{best_sales_hour} generates the highest "
        f"hourly revenue.\n"   
    )

    file.write(
        f"{best_value_hour} has the highest revenue "
        f"per customer.\n"
    )

    print("\nBusiness report saved to:")
    print(report_file)

# 15. CUSTOMER SALES RATIO

total_units_sold = sum(category_sales.values())

if total_entries > 0:
    sales_per_customer = total_units_sold / total_entries
else:
    sales_per_customer = 0
print("\nCUSTOMER SALES RATIO")
print("=" * 30)

print("TOTAL Units Sold:", total_units_sold)

print(
    "Units Sold per Customer:",
    round(sales_per_customer, 2)
)

# 16. CREATE DASHBOARD THEORY

dashboard_file = "outputs/dashboard_summary.csv"

with open(dashboard_file, "w", newline="") as file:

    writer = csv.writer(file)

    # Column headers
    writer.writerow([
        "Metric",
        "Value"
    ])

    # KPI values
    writer.writerow([
        "Total Customer Entries",
        total_entries
    ])

    writer.writerow([
        "Total Revenue",
        round(total_revenue, 2)
    ])

    writer.writerow([
        "Revenue per Customer",
        round(revenue_per_customer, 2)
    ])

    writer.writerow([
        "Best-Selling Category",
        best_category
    ])

    writer.writerow([
        "Units Sold",
        total_units_sold
    ])

    writer.writerow([
        "Highest Revenue Category",
        highest_revenue_category
    ])

    writer.writerow([
        "Highest Revenue Hour",
        best_sales_hour
    ])

    writer.writerow([
        "Highest Revenue per Customer Hour",
        best_value_hour
    ])

print("\nDashboard summary saved to:")
print(dashboard_file)    

# 17. ADVANCED PRODUCT PERFORMANCE ANALYSIS
 
product_performance = {}

for category in category_sales:

    units  = category_sales[category]
    revenue = category_revenue.get(category, 0)

    if units > 0:
        revenue_per_unit = revenue / units
    else:
        revenue_per_unit = 0

    if total_revenue > 0:
        revenue_share = (revenue / total_revenue) * 100
    else:
        revenue_share = 0

    product_performance[category] = {
        "units": units,
        "revenue": revenue,
        "revenue_per_unit": revenue_per_unit,
        "revenue_share": revenue_share
    }                

print("\nADVANCED PRODUCT PERFORMANCE")
print("=" * 35)

for category, data in product_performance.items():

    print("\nCategory:", category)
    print("Units Sold:", data["units"])
    print("Revenue: ₹", round(data["revenue"], 2))
    print(
        "Revenue per Unit: ₹",
        round(data["revenue_per_unit"], 2)
    )
    print(
        "Revenue Share:",
        round(data["revenue_share"], 2),
        "%"   
    )

# 18. PRODUCT PERFORMANCE REPORT

categories = list(product_performance.keys())

revenue_values = [
    product_performance[category]["revenue"]
    for category in categories
]

units_values = [
    product_performance[category]["units"]
    for category in categories
]

# Revenue by category
plt.figure(figsize=(8, 5))

plt.bar(categories, revenue_values)

plt.title("Product Category Revenue Performance")
plt.xlabel("Product Categories")
plt.ylabel("Revenue (₹)")

plt.tight_layout()

plt.savefig(
    "outputs/product_category_revenue_performance.png"
)
plt.show()

# Units sold by category
plt.figure(figsize=(8, 5))

plt.bar(categories, units_values)

plt.title("Product Category Sales Performance")
plt.xlabel("Product Category")
plt.ylabel("Units Sold")

plt.tight_layout()

plt.savefig(
    "outputs/product_category_units_performance.png"
)
plt.show()

# 19. REVENUE CONTRIBUTION ANALYSIS

print("\nREVENUE CONTRIBUTION ANALYSIS")
print("=" * 40)

for category, data in product_performance.items():

    revenue = data["revenue"]
    revenue_share = data["revenue_share"]

    print("\nCategory:", category)
    print("Revenue: ₹", round(revenue, 2))
    print("Revenue Contribution:", round(revenue_share, 2), "%")

# Identify the category with the highest revenue contribution

highest_contribution_category = max(
    product_performance,
    key=lambda category:
    product_performance[category]["revenue_share"]
)

highest_contribution = product_performance[
    highest_contribution_category
]["revenue_share"]

print("\nHighest Revenue Contributor:")
print(highest_contribution_category)

print(
    "Contribution:",
    round(highest_contribution, 2),
    "%"
)

# 20. REVENUE CONTRIBUTION  CHART

contribution_values = [
    product_performance[category]["revenue_share"]
    for category in categories
]

plt.figure(figsize=(8, 5))

plt.bar(categories, contribution_values)

plt.title("Revenue Contribution by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Revenue Contribution (%)")

plt.tight_layout()

plt.savefig(
    "outputs/revenue_contribution_by_category.png"
)

plt.show()    

# 21. SALES VS REVENUE ANALYIS

print("\nSALES VS REVENUE ANALYSIS")
print("=" * 40)

for category, data in product_performance.items():

    units = data["units"]
    revenue = data["revenue"]

    print("\nCategory:", category)
    print("Units Sold:", units)
    print("Revenue: ₹", round(revenue, 2))

    if units > 0:
        average_value_per_unit = revenue / units
    else:
        average_value_per_unit = 0

    print(
        "Average Revenue per Unit: ₹",
        round(average_value_per_unit, 2)
    )        

# Identify highest-value category per unit

highest_value_category = max(
    product_performance,
    key=lambda category:
    product_performance[category]["revenue_per_unit"]
)

print("\nHighest Revenue per Unit Category:")
print(highest_value_category)

print(
    "Revenue per Unit: ₹",
    round(
        product_performance[
            highest_value_category
        ]["revenue_per_unit"],
        2    
    )
)

# 22. CATEGORY PERFORMANCE RANKING

category_ranking = sorted(
    product_performance.items(),
    key=lambda item: item[1]["revenue"],
    reverse=True
)

print("\nCATEGORY PERFORMANCE RANKING")
print("=" * 40)

rank = 1

for category, data in category_ranking:

    print(
        f"{rank}. {category} "
        f"- Revenue: ₹{data['revenue']:.2f}"
    )

    rank += 1

# 23. CATEGORY PERFORMANCE SCORE

print("\nCATEGORY PERFORMANCE SCORE")
print("=" * 40)

total_units = sum(
    data["units"]
    for data in product_performance.values()
)

for category, data in product_performance.items():

    revenue_share = data["revenue_share"]

    if total_units > 0:
        sales_share = (data["units"] / total_units) * 100
    else:
        sales_share = 0

    performance_score = (
        revenue_share * 0.6
        + sales_share * 0.4
    )

    data["sales_share"] = sales_share
    data["performance_score"] = performance_score

    print("\nCategory:", category)
    print("Revenue Share:", round(revenue_share, 2), "%")
    print("Sales Share:", round(sales_share, 2), "%")
    print(
        "Performance Score:",
        round(performance_score, 2)
    )

# 24. CATEGORY PERFORMANCE SCORE CHART

performance_categories = list(product_performance.keys())

performance_scores = [
    product_performance[category]["performance_score"]
    for category in performance_categories
]

plt.figure(figsize=(8, 5))

plt.bar(
    performance_categories,
    performance_scores
)

plt.title("Category Performance Score")
plt.xlabel("Product Category")
plt.ylabel("Performance Score")

plt.tight_layout()

plt.savefig(
    "outputs/category_performance_score.png"
)

plt.show()    

# 25. AUTOMATED BUSINESS RECOMMENDATION

print("\nAUTOMATED BUSINESS RECOMMENDATION")
print("=" * 45)

best_category = max(
    product_performance,
    key=lambda category:
    product_performance[category]["performance_score"]
)

best_score = product_performance[
    best_category
]["performance_score"]

best_revenue = product_performance[
    best_category
]["revenue"]

best_units = product_performance[
    best_category
]["units"]

print("\nTop Performing Category:", best_category)
print("Performance Score:", round(best_score, 2))
print("Revenue: ₹", round(best_revenue, 2))
print("Units Sold:", best_units)

print("\nBusiness Recommendation:")

if best_score >= 50:
    print(
        f"Focus strongly on {best_category} because "
        f"it is the strongest overall performing category."
    )

elif best_score >= 30:
    print(
        f"Increase marketing and inventory attention for "
        f"{best_category} because it shows strong performance."
    )

else:
    print(
        f"Monitor {best_category} and evaluate strategies "
        f"to improve its overall performance."
    )

# 26. SAVE AUTOMATED BUSINESS INSIGHTS

with open(
    "outputs/automated_business_insights.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write("SMART RETAIL INTELLIGENCE\n")
    file.write("=========================\n\n")

    file.write(
        f"Top Performing Category: {best_category}\n"
    )

    file.write(
        f"Performance Score: {best_score:.2f}\n"
    )

    file.write(
        f"Revenue: ₹{best_revenue:.2f}\n"
    )

    file.write(
        f"Units Sold: {best_units}\n\n"
    )

    file.write("BUSINESS RECOMMENDATION\n")
    file.write("-----------------------\n")

    if best_score >= 50:
        recommendation = (
            f"Focus strongly on {best_category} because "
            f"it is the strongest overall performing category."
        )

    elif best_score >= 30:
        recommendation = (
            f"Increase marketing and inventory attention for "
            f"{best_category} because it shows strong performance."
        )

    else:
        recommendation = (
            f"Monitor {best_category} and evaluate strategies "
            f"to improve its overall performance."
        )

    file.write(recommendation + "\n")


print(
    "\nAutomated insights saved to "
    "outputs/automated_business_insights.txt"
)

# 27. EXPORT CATEGORY PERFORMANCE DATA

import csv

with open(
    "outputs/category_performance.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Product Category",
        "Units Sold",
        "Revenue",
        "Revenue per Unit",
        "Revenue Share (%)",
        "Sales Share (%)",
        "Performance Score"
    ])

    for category, data in product_performance.items():

        writer.writerow([
            category,
            data["units"],
            round(data["revenue"], 2),
            round(data["revenue_per_unit"], 2),
            round(data["revenue_share"], 2),
            round(data["sales_share"], 2),
            round(data["performance_score"], 2)
        ])

print(
    "\nCategory performance data saved to "
    "outputs/category_performance.csv"
)

# 28. PREPARE DATASET FOR AI/ML

print("\nPREPARING DATASET FOR AI/ML")
print("=" * 40)

print("ML dataset preparation is handled separately.")
print("Use src/ml_model.py for the AI/ML pipeline.")

# 29. LOAD ML-READY DATASET

print("\nML MODEL")
print("=" * 40)

print("The demand prediction model is trained using:")
print("ml_training_data.csv")

print("ML training and evaluation are handled in:")
print("src/ml_model.py")

# 30. ML PIPELINE

print("\nML MODELING")
print("=" * 40)

print("ML training and evaluation are handled in src/ml_model.py")

