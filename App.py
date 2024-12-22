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

# Memasukkan semua tabel ke dalam list
tables = [customers_data, products_data, orders_data]

# Menggabungkan tabel menggunakan outer join
main_data = pd.concat(tables, axis=1)

#Disini saya hanya cleaning dataset products karena hanya dataset ini yang memiliki missing values
main_data = main_data.dropna()

# mengurutkan main data berdasarkan order_id         
orders_data_sorted = main_data.sort_values(by='order_id', ascending=True)

#Judul Dashboard
st.title("Business Orders Dashboard")# Mengelompokkan data berdasarkan state dan menghitung jumlah pesanan
state_order_counts = main_data.groupby("customer_state")["customer_id"].count().reset_index()
state_order_counts.columns = ["State", "Number of Orders"]
state_order_counts = state_order_counts.sort_values(by="Number of Orders", ascending=False)

# Menghitung jumlah total pesanan untuk setiap state
total_orders = state_order_counts['Number of Orders'].sum()

# Mengelompokkan dan menjumlahkan untuk kategori "Other"
state_order_counts_grouped = state_order_counts.groupby('State')['Number of Orders'].sum().reset_index()

# Membuat Header
st.header("1. Kota (State) yang Memiliki Pesanan (Orders) Terbanyak")

# Membuat checkbox untuk semua state untuk filtering
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

# Menampilkan data yang telah ter-filter
st.subheader("Filtered States by Number of Orders")
st.write(filtered_data)

# Membuat pie chart untuk states yang telah ter-filter
fig_pie_chart = px.pie(
    filtered_data, 
    values="Number of Orders", 
    names="State",
    title="States Contribution by Number of Orders (Filtered)",
    hole=0.4, 
    labels={'State':'State', 'Number of Orders':'Number of Orders'},
    hover_data=["Number of Orders"]
)

# Menampilkan pie chart
st.subheader("Pie Chart: Filtered States by Number of Orders")
st.plotly_chart(fig_pie_chart)

# Mengelompokkan berdasarkan kategori produk dan menghitung total harga pesanan
category_price_totals = main_data.groupby("product_category_name")["price"].sum().reset_index()
category_price_totals.columns = ["Product Category", "Total Order Price"]
category_price_totals = category_price_totals.sort_values(by="Total Order Price", ascending=False)

# Menghitung jumlah total harga pesanan untuk setiap kategori produk
total_price = category_price_totals['Total Order Price'].sum()

# Menghitung persentase dan menggabungkan yang kurang dari 2% menjadi "Other"
category_price_totals['Percentage'] = (category_price_totals['Total Order Price'] / total_price) * 100
category_price_totals['Product Category'] = category_price_totals['Product Category'].where(category_price_totals['Percentage'] >= 2, 'Other')

# Mengelompokkan dan menjumlahkan untuk kategori "Other"
category_price_totals_grouped = category_price_totals.groupby('Product Category')['Total Order Price'].sum().reset_index()

# Membuat pie chart untuk semua kategori produk dengan kategori "Other"
fig_pie_chart_category = px.pie(
    category_price_totals_grouped, 
    values="Total Order Price", 
    names="Product Category",
    title="Product Categories Contribution by Total Order Price (Including 'Other'[sum that below 2%])",
    hole=0.4, 
    labels={'Product Category':'Product Category', 'Total Order Price':'Total Order Price'},
    hover_data=["Total Order Price"]
)

# Menampilkan subheader
st.header("2. Berapa Total Harga Pesanan per Kategori Produk?")

# Menampilkan 10 kategori teratas berdasarkan total harga pesanan
st.subheader("Top 10 Product Categories by Total Order Price")
st.write(category_price_totals.head(10))

# Membuat bar chart untuk total harga berdasarkan kategori produk
fig_category_price = px.bar(
    category_price_totals.head(10), 
    x="Product Category", 
    y="Total Order Price",
    title="Top 10 Product Categories by Total Order Price",
    color="Total Order Price"
)

st.plotly_chart(fig_category_price)

# Menampilkan diagram pie dengan persentase kontribusi
st.subheader("Pie Chart: Top 10 Product Categories by Total Order Price")

# Menampilkan pie chart di Streamlit
st.plotly_chart(fig_pie_chart_category)

















