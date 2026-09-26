import csv

csv_file = "customer_data.csv"

# Read customer data
with open(csv_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row)

# Calculate total entries
total_entries = 0

with open(csv_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total_entries = max(
            total_entries,
            int(row["Entered"])
        )

print("Total Entries:", total_entries)

# Find peak customers inside
peak_customers = 0

with open(csv_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        customers = int(row["Customers Inside"])

        if customers > peak_customers:
            peak_customers = customers

print("Peak Customers Inside:", peak_customers)

# Calculate total exits
total_exits = 0

with open(csv_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total_exits = max(
            total_exits,
            int(row["Exited"])
        )

print("Total Exits:", total_exits)

# Calculate current customers inside
customers_inside = total_entries - total_exits

print("Current Customers Inside:", customers_inside)

# Analyze footfall by time
hourly_entries = {}

with open(csv_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        timestamp = row["Timestamp"]
        hour = timestamp[:13]

        entered = int(row["Entered"])

        if hour not in hourly_entries:
            hourly_entries[hour] = entered
        else:
            hourly_entries[hour] = max(hourly_entries[hour], entered)    

print("\nfootfall by Hour:")  

for hour, entered in sorted(hourly_entries.items()):
    print(f"{hour}: {entered} entries")

# Find the busisest hour

if hourly_entries:
    busiest_hour = max(hourly_entries, key=hourly_entries.get)
    busiest_entries = hourly_entries[busiest_hour]

    print("\nBusiest Hour:", busiest_hour)
    print("Entries during Busiest Hour:", busiest_entries)
else:
    print("\nNO footfall data available.")  

import matplotlib.pyplot as plt

# Create footfall chart
hours = list(hourly_entries.keys())
entries = list(hourly_entries.values())

plt.figure(figsize=(10, 5))
plt.bar(hours, entries, color='blue')

plt.title("Customer Footfall by Hour")
plt.xlabel("Hour")
plt.ylabel("Number of Entries")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("outputs/footfall_by_hour.png")
plt.show()

# Create Entries vs Exits Chart
labels = ["Entries", "Exits"]
values = [total_entries, total_exits]

plt.figure(figsize=(7, 5))
plt.bar(labels, values)

plt.title("Customer Entries vs Exits")
plt.xlabel("Type")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig("outputs/entries_vs_exits.png")
plt.show()

# Generate business insights

with open("outputs/business_insights.txt", "w") as file:
    file.write("SMART RETAIL INTELLIGENCE - BUSINESS INSIGHTS\n")
    file.write("=" * 50 + "\n\n")

    file.write(f"Total Entries: {total_entries}\n")
    file.write(f"Total Exits: {total_exits}\n")
    file.write(f"Customers Currently Inside: {customers_inside}\n")
    file.write(f"Peak Customers Inside: {peak_customers}\n")
    file.write(f"Busiest Hour: {busiest_hour} with {busiest_entries} entries\n")
    file.write(f"Entries During Busiest Hour: {busiest_entries}\n")
    
print("\nBusiness insights saved to 'outputs/business_insights.txt'")
