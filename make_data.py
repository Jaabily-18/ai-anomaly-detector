import pandas as pd
import numpy as np

# Generate 30 days of synthetic sales data
dates = pd.date_range(start="2026-08-01", periods=30)
np.random.seed(42)

# Normal daily sales hover around $5,000 ± $300
normal_sales = np.random.normal(loc=5000, scale=300, size=30).round(2)

df = pd.DataFrame({
    "Date": dates.strftime("%Y-%m-%d"),
    "Region": "South",
    "Product": "SaaS Subscription",
    "Sales": normal_sales
})

# Plant two intentional anomalies for testing:
df.loc[12, "Sales"] = 1200.00   # Major drop (e.g., payment gateway failure)
df.loc[24, "Sales"] = 11500.00  # Massive spike (e.g., bulk enterprise deal)

df.to_csv("sales_data.csv", index=False)
print("✅ Created sales_data.csv with 2 planted anomalies!")