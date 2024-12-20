import streamlit as st
import pandas as pd

# Function to load data from GitHub
@st.cache_resource
def load_data_from_github():
    customers_url = 'https://raw.githubusercontent.com/akbarpradana/gdp-dashboard/main/data/customers_dataset.csv'  # CSV file
    products_url = 'https://raw.githubusercontent.com/akbarpradana/gdp-dashboard/main/data/products_dataset.csv'  # Excel file
    orders_url = 'https://raw.githubusercontent.com/akbarpradana/gdp-dashboard/main/data/order_items_dataset.csv'  # Excel file

    try:
        # Load the CSV file
        customers_data = pd.read_csv(customers_url)
        # Load the Excel files
        products_data = pd.read_csv(products_url)
        orders_data = pd.read_csv(orders_url)

        return customers_data, products_data, orders_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

# Load data
customers_data, products_data, orders_data = load_data_from_github()

if customers_data is not None and products_data is not None and orders_data is not None:
    # Title of the Dashboard
    st.title("Business Orders Dashboard")

    # 1. 10 states with the highest number of orders
    st.header("1. 10 States with the Highest Number of Orders")

    # Grouping states and counting orders
    state_order_counts = customers_data.groupby("customer_state")["customer_id"].count().reset_index()
    state_order_counts.columns = ["State", "Number of Orders"]
    state_order_counts = state_order_counts.sort_values(by="Number of Orders", ascending=False)

    # Display the top states
    st.subheader("Top States by Number of Orders")
    st.write(state_order_counts.head(10))

    # Displaying bar chart using Streamlit
    st.bar_chart(state_order_counts.set_index("State")["Number of Orders"].head(10))

    # 2. Total order price by product category
    st.header("2. Total Order Price by Product Category")

    # Merging orders_data and products_data
    merged_data = pd.merge(orders_data, products_data, on="product_id", how="left")

    # Grouping by product category and summing prices
    category_price_totals = merged_data.groupby("product_category_name")["price"].sum().reset_index()
    category_price_totals.columns = ["Product Category", "Total Order Price"]
    category_price_totals = category_price_totals.sort_values(by="Total Order Price", ascending=False)

    # Displaying the top product categories
    st.subheader("Top 10 Product Categories by Total Order Price")
    st.write(category_price_totals.head(10))

    # Creating a bar chart for total prices by product category using Streamlit
    st.bar_chart(category_price_totals.set_index("Product Category")["Total Order Price"].head(10))
else:
    st.info("Data could not be loaded. Please check the file paths.")
