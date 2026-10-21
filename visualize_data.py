from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "superstore.csv"
CHARTS_DIR = BASE_DIR / "charts"

CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# 1. LOAD DATA
# ==========================================
df = pd.read_csv(CSV_PATH)

# ==========================================
# 2. CATEGORY SALES ANALYSIS
# ==========================================
category_sales = df.groupby("Category")["Sales"].sum()

print("Category Sales:")
print(category_sales)

# ==========================================
# 3. CATEGORY PROFITABILITY ANALYSIS
# ==========================================
category_profit = df.groupby("Category")[["Sales", "Profit"]].sum()

category_profit["Profit Margin (%)"] = (
    category_profit["Profit"] / category_profit["Sales"] * 100
)

print("\nCategory Profit Margins:")
print(category_profit["Profit Margin (%)"].round(2))

# ==========================================
# 4. FURNITURE SUBCATEGORY ANALYSIS
# ==========================================
furniture_df = df[df["Category"] == "Furniture"]

furniture_profit = furniture_df.groupby("Sub-Category")["Profit"].sum()

print("\nFurniture Subcategory Profit:")
print(furniture_profit.round(2))

# ==========================================
# 5. FURNITURE DISCOUNT ANALYSIS
# ==========================================
discount_summary = furniture_df.groupby("Discount")[["Sales", "Profit"]].sum()

discount_summary["Profit Margin (%)"] = (
    discount_summary["Profit"] / discount_summary["Sales"] * 100
)

discount_summary["Record Count"] = furniture_df.groupby("Discount").size()

print("\nFurniture Profit Margin by Discount:")
print(discount_summary.round(2))

# ==========================================
# 6. CATEGORY SALES CHART
# ==========================================
ax = category_sales.plot(kind="bar")

for bar in ax.patches:
    height = bar.get_height()
    ax.annotate(
        f"${height / 1000:,.1f}K",
        (bar.get_x() + bar.get_width() / 2, height),
        ha="center",
        va="bottom",
        xytext=(0, 5),
        textcoords="offset points"
    )
# Leave enough space above the bars for value labels
ax.set_ylim(0, category_sales.max() * 1.15)
plt.title("Total Sales by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Sales ($)")
plt.xticks(rotation=0)

ax.yaxis.set_major_formatter(
    FuncFormatter(lambda value, position: f"${value / 1000:,.0f}K")
)

plt.tight_layout()
plt.savefig(CHARTS_DIR / "category_sales.png", dpi=300, bbox_inches="tight")
plt.close()

# ==========================================
# 7. CATEGORY PROFIT MARGIN CHART
# ==========================================
plt.figure()

colors = ["#D95F59", "#4C78A8", "#4C78A8"]

ax2 = category_profit["Profit Margin (%)"].plot(
    kind="bar",
    color=colors
)

for bar in ax2.patches:
    height = bar.get_height()

    ax2.annotate(
        f"{height:.2f}%",
        (bar.get_x() + bar.get_width() / 2, height),
        ha="center",
        va="bottom",
        xytext=(0, 5),
        textcoords="offset points"
    )
# Leave space above the bars for percentage labels
ax2.set_ylim(0, category_profit["Profit Margin (%)"].max() * 1.15)
plt.title("Profit Margin by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Profit Margin (%)")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig(CHARTS_DIR / "category_profit_margin.png", dpi=300, bbox_inches="tight")
plt.close()

# ==========================================
# 8. FURNITURE SUBCATEGORY PROFIT CHART
# ==========================================
plt.figure()

colors = [
    "#D95F59" if profit < 0 else "#4C78A8"
    for profit in furniture_profit
]

ax3 = furniture_profit.plot(
    kind="bar",
    color=colors
)

for bar in ax3.patches:
    height = bar.get_height()

    ax3.annotate(
        f"${height:,.0f}",
        (bar.get_x() + bar.get_width() / 2, height),
        ha="center",
        va="bottom" if height >= 0 else "top",
        xytext=(0, 5 if height >= 0 else -5),
        textcoords="offset points"
    )
# Leave room for labels above profits and below losses
ax3.set_ylim(
    furniture_profit.min() * 1.20,
    furniture_profit.max() * 1.20
)
plt.title("Furniture Profit and Loss by Subcategory")
plt.xlabel("Furniture Subcategory")
plt.ylabel("Total Profit ($)")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig(
    CHARTS_DIR / "furniture_subcategory_profit.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

# ==========================================
# 9. FURNITURE DISCOUNT VS PROFIT MARGIN
# ==========================================
plt.figure()

plt.plot(
    discount_summary.index * 100,
    discount_summary["Profit Margin (%)"],
    marker="o"
)
plt.axhline(
    y=0,
    color="red",
    linestyle="--",
    linewidth=1
)
plt.title("Furniture Profit Margin by Discount Level")
plt.xlabel("Discount (%)")
plt.ylabel("Profit Margin (%)")
plt.xticks(range(0, 71, 10))
plt.tight_layout()
plt.savefig(
    CHARTS_DIR / "furniture_discount_profit_margin.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()