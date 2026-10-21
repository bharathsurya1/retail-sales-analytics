-- ==========================================
-- 1. CATEGORY SALES AND PROFITABILITY
-- Business Question:
-- Which product categories generate the most
-- revenue, and how profitable are they?
-- ==========================================

SELECT
    Category,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(
        SUM(Profit) * 100.0 / SUM(Sales),
        2
    ) AS profit_margin
FROM orders
GROUP BY Category
ORDER BY profit_margin DESC;


-- ==========================================
-- 2. FURNITURE SUBCATEGORY PROFITABILITY
-- Business Question:
-- Which Furniture subcategories generated
-- over $100,000 in sales but have profit
-- margins below 10%?
-- ==========================================

SELECT
    "Sub-Category",
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(
        SUM(Profit) * 100.0 / SUM(Sales),
        2
    ) AS profit_margin
FROM orders
WHERE Category = 'Furniture'
GROUP BY "Sub-Category"
HAVING
    SUM(Sales) > 100000
    AND SUM(Profit) * 100.0 / SUM(Sales) < 10
ORDER BY profit_margin ASC;


-- ==========================================
-- 3. AVERAGE ORDER VALUE
-- Business Question:
-- How much revenue does each distinct
-- customer order generate on average?
-- ==========================================

SELECT
    ROUND(SUM(Sales), 2) AS total_sales,
    COUNT(DISTINCT "Order ID") AS total_orders,
    ROUND(
        SUM(Sales) / COUNT(DISTINCT "Order ID"),
        2
    ) AS average_order_value
FROM orders;


-- ==========================================
-- 4. PROFITABILITY DISTRIBUTION
-- Business Question:
-- What percentage of order-line records
-- are profitable, loss-making, or break-even?
-- ==========================================

SELECT
    CASE
        WHEN Profit > 0 THEN 'Profitable'
        WHEN Profit < 0 THEN 'Loss'
        ELSE 'Break-even'
    END AS profit_status,
    COUNT(*) AS record_count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM orders
GROUP BY profit_status;


-- ==========================================
-- 5. CATEGORY LOSS RATE ANALYSIS
-- Business Question:
-- What percentage of order-line records
-- are loss-making in each product category?
-- ==========================================

WITH profit_classification AS (
    SELECT
        Category,
        CASE
            WHEN Profit > 0 THEN 'Profitable'
            WHEN Profit < 0 THEN 'Loss'
            ELSE 'Break-even'
        END AS profit_status
    FROM orders
),
category_summary AS (
    SELECT
        Category,
        COUNT(*) AS total_records,
        SUM(
            CASE
                WHEN profit_status = 'Loss' THEN 1
                ELSE 0
            END
        ) AS loss_records
    FROM profit_classification
    GROUP BY Category
)
SELECT
    Category,
    total_records,
    loss_records,
    ROUND(
        loss_records * 100.0 / total_records,
        2
    ) AS loss_percentage
FROM category_summary
ORDER BY loss_percentage DESC;


-- ==========================================
-- 6. MONTH-OVER-MONTH REVENUE GROWTH
-- Business Question:
-- How does monthly revenue change compared
-- with the previous month?
-- ==========================================

WITH monthly_sales AS (
    SELECT
        strftime('%Y-%m', "Order Date") AS order_month,
        ROUND(SUM(Sales), 2) AS total_sales,
        COUNT(DISTINCT "Order ID") AS total_orders
    FROM orders
    GROUP BY order_month
),
monthly_comparison AS (
    SELECT
        order_month,
        total_sales,
        LAG(total_sales) OVER (
            ORDER BY order_month
        ) AS previous_month_sales
    FROM monthly_sales
)
SELECT
    order_month,
    total_sales,
    previous_month_sales,
    ROUND(
        (total_sales - previous_month_sales) * 100.0
        / NULLIF(previous_month_sales, 0),
        2
    ) AS mom_growth_percentage
FROM monthly_comparison
ORDER BY order_month ASC;


 -- ============================================================
-- Query 7: Annual Sales and Profitability Analysis
-- Business Question:
-- How did annual revenue, profit, order volume, and profit
-- margin change between 2015 and 2018?
-- ============================================================

SELECT
    STRFTIME('%Y', "Order Date") AS order_year,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    COUNT(DISTINCT "Order ID") AS total_orders,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS profit_margin
FROM orders
GROUP BY order_year
ORDER BY order_year ASC;


-- ============================================================
-- Query 8: Year-over-Year Revenue Growth
-- Business Question:
-- How much did annual revenue increase or decrease compared
-- with the previous year?
-- ============================================================

WITH annual_sales AS (
    SELECT
        STRFTIME('%Y', "Order Date") AS order_year,
        ROUND(SUM(Sales), 2) AS total_sales
    FROM orders
    GROUP BY order_year
),
annual_comparison AS (
    SELECT
        order_year,
        total_sales,
        LAG(total_sales) OVER (
            ORDER BY order_year
        ) AS previous_year_sales
    FROM annual_sales
)
SELECT
    order_year,
    total_sales,
    previous_year_sales,
    ROUND(
        (total_sales - previous_year_sales) * 100.0
        / NULLIF(previous_year_sales, 0),
        2
    ) AS annual_growth_percentage
FROM annual_comparison
ORDER BY order_year;


-- ============================================================
-- Query 9: Annual Average Order Value Analysis
-- Business Question:
-- How did average order value change each year, and was
-- revenue growth driven by more orders or larger orders?
-- ============================================================

SELECT
    STRFTIME('%Y', "Order Date") AS order_year,
    ROUND(SUM(Sales), 2) AS total_sales,
    COUNT(DISTINCT "Order ID") AS total_orders,
    ROUND(
        SUM(Sales) * 1.0 / COUNT(DISTINCT "Order ID"),
        2
    ) AS average_order_value
FROM orders
GROUP BY order_year
ORDER BY order_year ASC;


-- ============================================================
-- Query 10: Annual Category Revenue and Profitability
-- Business Question:
-- How did revenue, profit, and profit margin change across
-- product categories each year?
-- ============================================================

SELECT
    STRFTIME('%Y', "Order Date") AS order_year,
    Category AS category,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(
        SUM(Profit) * 100.0 / SUM(Sales),
        2
    ) AS profit_margin
FROM orders
GROUP BY order_year, Category
ORDER BY order_year ASC, total_sales DESC;


-- ============================================================
-- Query 11: Top Customers by Revenue and Profitability
-- Business Question:
-- Which customers generate the most revenue, and how
-- profitable are those customer relationships?
-- ============================================================

WITH customer_performance AS (
    SELECT
        c."Customer ID" AS customer_id,
        c."Customer Name" AS customer_name,
        COUNT(DISTINCT o."Order ID") AS total_orders,
        ROUND(SUM(o.Sales), 2) AS total_sales,
        ROUND(SUM(o.Profit), 2) AS total_profit
    FROM customers c
    INNER JOIN orders o
        ON c."Customer ID" = o."Customer ID"
    GROUP BY
        c."Customer ID",
        c."Customer Name"
)
SELECT
    customer_id,
    customer_name,
    total_orders,
    total_sales,
    total_profit,
    ROUND(
        total_profit * 100.0 / NULLIF(total_sales, 0),
        2
    ) AS profit_margin_pct
FROM customer_performance
ORDER BY total_sales DESC, customer_id
LIMIT 10;


-- ============================================================
-- Query 12: Top Revenue Products Within Each Category
-- Business Question:
-- Which three products generate the highest revenue
-- in each category, and are they profitable?
-- ============================================================

WITH product_performance AS (
    SELECT
        Category AS category,
        "Product ID" AS product_id,
        "Product Name" AS product_name,
        ROUND(SUM(Sales), 2) AS total_sales,
        ROUND(SUM(Profit), 2) AS total_profit
    FROM orders
    GROUP BY
        Category,
        "Product ID",
        "Product Name"
),
ranked_products AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY total_sales DESC, product_id, product_name
        ) AS revenue_rank
    FROM product_performance
)
SELECT
    category,
    revenue_rank,
    product_id,
    product_name,
    total_sales,
    total_profit,
    ROUND(
        total_profit * 100.0 / NULLIF(total_sales, 0),
        2
    ) AS profit_margin_pct
FROM ranked_products
WHERE revenue_rank <= 3
ORDER BY category, revenue_rank;