
# Retail Sales & Profitability Analytics

## Project Overview
An end-to-end data analytics project focused on understanding retail sales performance, profitability, and business trends.

## Business Objectives
- Analyze sales and revenue trends.
- Identify high-performing products and categories.
- Evaluate profitability across different segments.
- Discover opportunities to improve business performance.

## Dataset

This project uses the publicly shared Sample Superstore dataset,
containing 9,994 order-line records and 21 original columns.

The dataset includes order dates, shipping information, customer
segments, product categories, sales, quantities, discounts, and profit.

**Dataset source:**
[Sample Superstore — GitHub Gist](https://gist.github.com/LeDangHoangLongVu/facde0e42cd6a5e2b55f2287d34fc6b8)

The original CSV is not included in this repository.
To reproduce the analysis, download the dataset from the source
above and save the CSV as `data/superstore.csv`.

### Data Quality

- Total records: 9,994
- Original columns: 21
- Missing values: 11 records have missing Postal Code values
- Duplicate rows: 0
- Duplicate Row IDs: 0
- Shipping duration: 0–7 days, averaging 3.96 days

Missing Postal Code values were retained because they do not
prevent sales and profitability analysis.

This is a sample dataset used for educational and portfolio purposes.
Findings should not be interpreted as actual business performance
or validated causal relationships.

## Getting Started

### Prerequisites

- Python 3.11
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/bharathsurya1/retail-sales-analytics.git
cd retail-sales-analytics
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

For Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Download the Dataset

Download the Sample Superstore CSV from the dataset source
linked above.

Save the CSV in the following location:

```text
data/superstore.csv
```

Create the `data` directory if it does not exist.

### 5. Run the Python Analysis

```bash
python explore_data.py
```

This displays data-quality checks, business KPIs,
category profitability, and Furniture discount analysis.

### 6. Generate Visualizations

```bash
python visualize_data.py
```

This generates four PNG charts in the `charts/` directory.

### 7. Create the SQLite Database

```bash
python setup_database.py
```

This creates `data/superstore.db` and imports 9,994 records
into the `orders` table.

The SQL analysis queries are available in:

```text
sql/retail_analysis.sql
```

These queries can be executed against the generated SQLite
database using a compatible SQLite client.

## Tools and Technologies
- SQL
- Python (pandas, matplotlib)
- Power BI (dashboard development planned)
- SQLite
- Git and GitHub

## Project Status

**In Progress — Dashboard Development**

Completed:
- Python data exploration and data-quality checks
- Sales, profitability, and discount analysis
- Four Matplotlib visualizations
- SQLite database setup
- 10 documented and tested SQL queries

Remaining:
- Interactive Power BI dashboard
- Final business recommendations
- Reproducibility testing and GitHub documentation review

## Project Deliverables

- `explore_data.py` — Python data exploration and business analysis
- `visualize_data.py` — Generates four analytical charts
- `setup_database.py` — Builds the SQLite database
- `sql/retail_analysis.sql` — 10 documented SQL queries
- `charts/` — Four visualizations
- Power BI dashboard — Planned

## Key Findings

### 1. Furniture Profitability and Discounts

The Superstore dataset contains 9,994 order-line records, with approximately $2.30 million in total sales and $286,397 in recorded profit, resulting in an overall profit margin of 12.47%.

Furniture generated approximately $742,000 in sales but achieved a profit margin of only 2.49%, compared with 17.04% for Office Supplies and 17.40% for Technology.

Further analysis identified Tables as the largest loss-making Furniture subcategory, with a total loss of approximately $17,725.

An analysis of Furniture discounts found that every observed discount group at 30% or higher had a negative aggregate profit margin, whereas all groups at 20% or lower remained profitable. Some higher-discount groups contained relatively few records, so their individual margins should be interpreted cautiously.

**Business implication:** Review discount policies for loss-making Furniture products, particularly Tables, and investigate product costs and pricing before making changes. The observed relationship does not establish that discounting alone caused the losses.

## Data Visualizations

### 1. Total Sales by Category
![Total Sales by Category](charts/category_sales.png)

### 2. Profit Margin by Category
![Profit Margin by Category](charts/category_profit_margin.png)

### 3. Furniture Subcategory Profit and Loss
![Furniture Subcategory Profit](charts/furniture_subcategory_profit.png)

### 4. Furniture Discount vs. Profit Margin
![Furniture Discount vs Profit Margin](charts/furniture_discount_profit_margin.png)