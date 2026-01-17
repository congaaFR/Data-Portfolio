import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# 1. Load Data
# We use a direct link to the Superstore dataset
url = "https://raw.githubusercontent.com/adverity/learning-datasets/main/superstore.csv"

print("Loading data from URL...")

try:
    # 'latin1' encoding is used to handle special characters
    df = pd.read_csv(url, encoding='latin1')
    print(f"Success: {len(df)} rows loaded.")
except Exception as e:
    print(f"Error loading data: {e}")
    exit()

# 2. Data Cleaning & Preparation
# Convert the date column to proper datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

# Aggregate sales by Month (Sum of sales per month)
monthly_sales = df.set_index('Order Date').resample('MS')['Sales'].sum().reset_index()

print("\nMonthly Sales Preview:")
print(monthly_sales.head())

# 3. Machine Learning (Prediction)
# We prepare features: Year and Month
monthly_sales['Month_Num'] = monthly_sales['Order Date'].dt.month
monthly_sales['Year'] = monthly_sales['Order Date'].dt.year

X = monthly_sales[['Year', 'Month_Num']]
y = monthly_sales['Sales']

# Train the Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 4. Predict Future Sales
# We predict sales for January of the next year
future_year = monthly_sales['Year'].max() + 1
future_month = 1 

prediction = model.predict([[future_year, future_month]])[0]

print(f"\nPrediction for January {future_year}: ${prediction:,.2f}")

# 5. Export Data
monthly_sales.to_csv('cleaned_sales_data.csv', index=False)
print("File 'cleaned_sales_data.csv' saved successfully.")

