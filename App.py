import streamlit as st
import pandas as pd

# Function to load data from GitHub
@st.cache_resource
def load_data_from_github():
    customers_url = 'https://raw.githubusercontent.com/akbarpradana/gdp-dashboard/main/data/customers_dataset.csv'  # CSV file
    products_url = 'https://raw.githubusercontent.com/akbarpradana/gdp-dashboard/main/data/products_dataset.csv'  # Excel file
    orders_url = 'https://raw.githubusercontent.com/akbarpradana/gdp-dashboard/main/data/order_items_dataset.csv'  # Excel file

    # Load the CSV file
    customers_data = pd.read_csv(customers_url)
    # Load the Excel files
    products_data = pd.read_csv(products_url)
    orders_data = pd.read_csv(orders_url)

    return customers_data, products_data, orders_data


# Load data
customers_data, products_data, orders_data = load_data_from_github()
# 1. Menmpilkan state                   
# Mengelompokkan kota (state) dan menghitung jumlah pesanan
state_order_counts = customers_data.groupby("customer_state")["customer_id"].count().reset_index()
state_order_counts.columns = ["State", "Number of Orders"]
state_order_counts = state_order_counts.sort_values(by="Number of Orders", ascending=False)

# Menghitung jumlah total pesanan untuk setiap kota
total_orders = state_order_counts['Number of Orders'].sum()

# Mengelompokkan dan menjumlahkan untuk kategori "Other"
state_order_counts_grouped = state_order_counts.groupby('State')['Number of Orders'].sum().reset_index()

st.title("Business Orders Dashboard")


 # Membuat Header         
st.header("1.  Berapa jumlah order (pesanan) setiap State (kota) dan presentasenya?")

# membuat checkbox untuk semua state untuk filtering   
selected_states = st.multiselect(
    "Select States to Filter",
    options=state_order_counts_grouped['State'].unique(),
    default=state_order_counts_grouped['State'].unique()[:2]  # Default to first two states
)

# Membuat slider untuk filtering range order      
min_orders, max_orders = st.slider(
    "Select the range of Number of Orders",
    min_value=int(state_order_counts_grouped['Number of Orders'].min()),
    max_value=int(state_order_counts_grouped['Number of Orders'].max()),
    value=(0, int(state_order_counts_grouped['Number of Orders'].max()))  # Default to full range
)

# Filter data berdasarkan filter di atas
filtered_data = state_order_counts_grouped[
    (state_order_counts_grouped['State'].isin(selected_states)) &
    (state_order_counts_grouped['Number of Orders'].between(min_orders, max_orders))
]

# menampilkan data yang terlah ter-filter        
st.subheader("Filtered States by Number of Orders")
st.write(filtered_data)

# Membuat piechart             
fig_pie_chart = px.pie(filtered_data, values="Number of Orders", names="State",
                       title="States Contribution by Number of Orders (Filtered)",
                       hole=0.4, labels={'State':'State', 'Number of Orders':'Number of Orders'},
                       hover_data=["Number of Orders"])

# Menampilkan pie chart
st.subheader("Pie Chart: Filtered States by Number of Orders")
st.plotly_chart(fig_pie_chart)
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
