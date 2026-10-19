import pandas as pd

# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("data/superstore.csv")


# ==========================================
# 2. DATA PREPARATION
# ==========================================

# Convert date columns from strings to datetime
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%Y-%m-%d")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%Y-%m-%d")

# Calculate the number of days between ordering and shipping
df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days


# ==========================================
# 3. DATA QUALITY CHECKS
# ==========================================

missing_values = df.isna().sum()
duplicate_rows = df.duplicated().sum()
duplicate_row_ids = df["Row ID"].duplicated().sum()

shipping_min = df["Shipping Days"].min()
shipping_max = df["Shipping Days"].max()
shipping_avg = df["Shipping Days"].mean()


# ==========================================
# 4. BUSINESS KPIs
# ==========================================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_units = df["Quantity"].sum()

profit_margin = (total_profit / total_sales) * 100

print("Total Sales:", round(total_sales, 2))
print("Total Profit:", round(total_profit, 2))
print("Total Units Sold:", total_units)
print("Overall Profit Margin:", round(profit_margin, 2), "%")


# ==========================================
# 5. CATEGORY ANALYSIS
# ==========================================

category_summary = df.groupby("Category")[["Sales", "Profit"]].sum()

category_summary["Profit Margin (%)"] = (
    category_summary["Profit"] / category_summary["Sales"] * 100
).round(2)

print("\nCategory Performance:")
print(category_summary)


# ==========================================
# 6. FURNITURE SUBCATEGORY ANALYSIS
# ==========================================

furniture_df = df[df["Category"] == "Furniture"]

furniture_summary = furniture_df.groupby("Sub-Category")[["Sales", "Profit"]].sum()

average_discounts = furniture_df.groupby("Sub-Category")["Discount"].mean()

print("\nFurniture Subcategory Performance:")
print(furniture_summary)

print("\nAverage Discount by Furniture Subcategory:")
print((average_discounts * 100).round(2))


# ==========================================
# 7. DISCOUNT PROFITABILITY ANALYSIS
# ==========================================

discount_profit = furniture_df.groupby("Discount")[["Sales", "Profit"]].sum()

discount_profit["Profit Margin (%)"] = (
    discount_profit["Profit"] / discount_profit["Sales"] * 100
).round(2)

discount_profit["Record Count"] = furniture_df.groupby("Discount").size()

print("\nFurniture Profitability by Discount Level:")
print(discount_profit)