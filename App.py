import streamlit as st
import pandas as pd

# Function to load data from GitHub
@st.cache_resource
def load_data_from_github():
    customers_url = 'https://raw.githubusercontent.com/akbarpradana/gdp-dashboard/main/data/customers_dataset.csv'
    products_url = 'https://raw.githubusercontent.com/akbarpradana/gdp-dashboard/main/data/products_dataset.csv'
    orders_url = 'https://raw.githubusercontent.com/akbarpradana/gdp-dashboard/main/data/order_items_dataset.csv'

    customers_data = pd.read_csv(customers_url)
    products_data = pd.read_csv(products_url)
    orders_data = pd.read_csv(orders_url)

    return customers_data, products_data, orders_data

# Load data
customers_data, products_data, orders_data = load_data_from_github()

# Grouping and counting orders by state
state_order_counts = customers_data.groupby("customer_state")["customer_id"].count().reset_index()
state_order_counts.columns = ["State", "Number of Orders"]
state_order_counts = state_order_counts.sort_values(by="Number of Orders", ascending=False)

# Grouping and summing for the selected states
state_order_counts_grouped = state_order_counts.groupby('State')['Number of Orders'].sum().reset_index()

st.title("Business Orders Dashboard")

# Creating a multiselect for filtering states
selected_states = st.multiselect(
    "Select States to Filter",
    options=state_order_counts_grouped['State'].unique(),
    default=state_order_counts_grouped['State'].unique()[:2]
)

# Creating a slider for filtering range of orders
min_orders, max_orders = st.slider(
    "Select the range of Number of Orders",
    min_value=int(state_order_counts_grouped['Number of Orders'].min()),
    max_value=int(state_order_counts_grouped['Number of Orders'].max()),
    value=(0, int(state_order_counts_grouped['Number of Orders'].max()))
)

# Filter data based on the selections
filtered_data = state_order_counts_grouped[
    (state_order_counts_grouped['State'].isin(selected_states)) &
    (state_order_counts_grouped['Number of Orders'].between(min_orders, max_orders))
]

# Display filtered data
st.subheader("Filtered States by Number of Orders")
st.write(filtered_data)

# Create a bar chart visualization
if not filtered_data.empty:
    filtered_data['Proportion'] = filtered_data['Number of Orders'] / filtered_data['Number of Orders'].sum()
    st.subheader("Bar Chart: Filtered States by Number of Orders (as Bar Chart)")
    st.bar_chart(filtered_data.set_index('State')['Proportion'])

    # Create a pie chart visualization
    st.subheader("Pie Chart: Filtered States by Number of Orders")
    st.pyplot(filtered_data.set_index('State')['Number of Orders'].plot.pie(autopct='%1.1f%%', startangle=90))
else:
    st.warning("No data available for the selected filters.")

# Total order price by product category
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
