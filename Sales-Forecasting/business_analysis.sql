/* SALES DATA ANALYSIS
   Dataset: Superstore Real Retail Data
*/

-- 1. Best Selling Categories
-- Which product category generates the most revenue?
SELECT 
    Category,
    SUM(Sales) as Total_Revenue
FROM superstore_sales
GROUP BY Category
ORDER BY Total_Revenue DESC;

-- 2. Seasonal Trends
-- Calculate average sales per month to find peak seasons
SELECT 
    MONTH(Order_Date) as Month_Number,
    AVG(Sales) as Avg_Sales
FROM superstore_sales
GROUP BY Month_Number
ORDER BY Avg_Sales DESC;

-- 3. Top Customers
-- Identify customers with total spending over 5000
SELECT 
    Customer_ID,
    SUM(Sales) as Total_Spend
FROM superstore_sales
GROUP BY Customer_ID
HAVING Total_Spend > 5000
ORDER BY Total_Spend DESC;
