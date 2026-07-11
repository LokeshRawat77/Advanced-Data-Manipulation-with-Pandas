import pandas as pd
import matplotlib.pyplot as plt
import os

# Create folders
os.makedirs("visualizations", exist_ok=True)
os.makedirs("report", exist_ok=True)

try:
    # Load dataset
    df = pd.read_csv("data/sales_data.csv")

    # -----------------------------
    # Data Exploration
    # -----------------------------
    print("\nFirst 5 Rows")
    print(df.head())

    print("\nDataset Info")
    print(df.info())

    print("\nMissing Values")
    print(df.isnull().sum())

    # -----------------------------
    # Data Cleaning
    # -----------------------------
    df = df.drop_duplicates()
    df["Date"] = pd.to_datetime(df["Date"])

    df["Month"] = df["Date"].dt.month_name()
    df["Year"] = df["Date"].dt.year

    # -----------------------------
    # Customer Analysis
    # -----------------------------
    top_customers = (
        df.groupby("Customer_ID")["Total_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\nTop Customers")
    print(top_customers)

    # -----------------------------
    # Product Analysis
    # -----------------------------
    product_sales = (
        df.groupby("Product")["Total_Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nProduct Sales")
    print(product_sales)

    # -----------------------------
    # Regional Analysis
    # -----------------------------
    regional_sales = (
        df.groupby("Region")["Total_Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nRegional Sales")
    print(regional_sales)

    # -----------------------------
    # Monthly Sales
    # -----------------------------
    monthly_sales = (
        df.groupby("Month")["Total_Sales"]
        .sum()
    )

    print("\nMonthly Sales")
    print(monthly_sales)

    # -----------------------------
    # Pivot Table
    # -----------------------------
    pivot = pd.pivot_table(
        df,
        values="Total_Sales",
        index="Region",
        columns="Product",
        aggfunc="sum",
        fill_value=0
    )

    print("\nPivot Table")
    print(pivot)

    # -----------------------------
    # Charts
    # -----------------------------

    # Monthly Sales
    plt.figure(figsize=(8,5))
    monthly_sales.plot(kind="line", marker="o")
    plt.title("Monthly Sales")
    plt.tight_layout()
    plt.savefig("visualizations/monthly_sales.png")
    plt.close()

    # Product Sales
    plt.figure(figsize=(8,5))
    product_sales.plot(kind="bar")
    plt.title("Product Sales")
    plt.tight_layout()
    plt.savefig("visualizations/product_sales.png")
    plt.close()

    # Regional Sales
    plt.figure(figsize=(7,7))
    regional_sales.plot(kind="pie", autopct="%1.1f%%")
    plt.ylabel("")
    plt.title("Regional Sales")
    plt.tight_layout()
    plt.savefig("visualizations/regional_sales.png")
    plt.close()

    # Top Customers
    plt.figure(figsize=(10,5))
    top_customers.plot(kind="bar")
    plt.title("Top Customers")
    plt.tight_layout()
    plt.savefig("visualizations/top_customers.png")
    plt.close()

    # Save Report
    with open("report/business_report.md","w") as f:
        f.write("# Customer Sales Analysis\n\n")
        f.write(f"Total Revenue : ₹{df['Total_Sales'].sum():,.2f}\n\n")
        f.write(f"Best Product : {product_sales.idxmax()}\n\n")
        f.write(f"Highest Sales Region : {regional_sales.idxmax()}\n\n")
        f.write("## Insights\n")
        f.write("- Top customers contribute the highest revenue.\n")
        f.write("- Laptop is the best-selling product.\n")
        f.write("- North region has the highest sales.\n")
        f.write("- Monthly sales trends help identify seasonal demand.\n")

    print("\nProject Completed Successfully!") 

except FileNotFoundError:
    print("data/sales_data.csv file not found!")

except Exception as e:
    print("Error:", e)