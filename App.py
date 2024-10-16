

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyngrok import ngrok
from google.colab import drive

@st.cache_resource
def load_customers_data():
    return pd.read_csv("/content/gdrive/MyDrive/E-Commerce Public Dataset/customers_dataset.csv", sep=',')

@st.cache_resource
def load_products_data():
    return pd.read_csv("/content/gdrive/MyDrive/E-Commerce Public Dataset/products_dataset.csv", sep=',')

@st.cache_resource
def load_orders_data():
    return pd.read_csv("/content/gdrive/MyDrive/E-Commerce Public Dataset/order_items_dataset.csv", sep=',')
customers_data = load_customers_data()
products_data = load_products_data()
orders_data = load_orders_data()
#Judul Dashboard
st.title("Business Orders Dashboard")

# 1. 5 kota (state) yang memiliki pesanan (orders) terbanyak
st.header("1. 10 kota (state) yang memiliki pesanan (orders) terbanyak?")

# mengelompokkan kota dan menjumlahkan pesanannya
state_order_counts = customers_data.groupby("customer_state")["customer_id"].count().reset_index()
state_order_counts.columns = ["State", "Number of Orders"]
state_order_counts = state_order_counts.sort_values(by="Number of Orders", ascending=False)

# menampilkan 5 kota yang memiliki pesanan terbanyak
st.subheader("Top States by Number of Orders")
st.write(state_order_counts.head(5))

# menampilkan bar chart
fig_state_orders = px.bar(state_order_counts, x="State", y="Number of Orders",
                          title="State-wise Number of Orders", color="Number of Orders")
st.plotly_chart(fig_state_orders)

# Berapa total harga pesanan per kategori produk?
st.header("2. Berapa total harga pesanan per kategori produk?")

# mennggabungkan orders_data dan products_data
merged_data = pd.merge(orders_data, products_data, on="product_id", how="left")

# menggelompokkan product percategory product dan menjumlahkan harga pesanannya
category_price_totals = merged_data.groupby("product_category_name")["price"].sum().reset_index()
category_price_totals.columns = ["Product Category", "Total Order Price"]
category_price_totals = category_price_totals.sort_values(by="Total Order Price", ascending=False)


# Menampilkan 10 kategori teratas berdasarkan total harga pesanan
st.subheader("Top 10 Product Categories by Total Order Price")
st.write(category_price_totals.head(10))

# membuat bar chart untuk total harga berdasarkan kategori produk
fig_category_price = px.bar(category_price_totals.head(10), x="Product Category", y="Total Order Price",
                            title="Top 10 Product Categories by Total Order Price", color="Total Order Price")
st.plotly_chart(fig_category_price)

