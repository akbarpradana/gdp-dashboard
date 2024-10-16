# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sBjgbwisUzrr6oWvGYMTV-sMFLdQCGCU

#Proyek Analisis Data : E-Commerce Public Dataset


*   Nama        : Akbar Wahyu Pradana
*   Email       : m200b4ky0281@bangkit.academy
*   ID Dicoding : Akbar Wahyu Pradana M200B4KY0281

## Menetukaan Pertanyaan Bisnis

1. 5 State (kota) mana yang memiliki order (pesanan) terbanyak
2. 10 terbanyak order (pesanan) berdasarkan kategori pesananan

## Import Semua Packages/Library yang Digunakan
"""

pip install pandas
pip install plotly
pip install streamlit -q


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from google.colab import drive

pip install pipreqs


drive.mount('/content/gdrive')

"""## Data Wrangling

### Gathering Data
"""

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

"""###Assesing Data

#### Memeriksa Missing Values
"""

#CUSTOMER
print("Missing Values pada Customers Dataset")
missing_values_customer = customers_data.isnull().sum()

print(missing_values_customer)

#PRODUCTS
print("Missing Values pada Product Dataset")
missing_values_product = products_data.isnull().sum()

print(missing_values_product)

#Order
print("Missing Values pada Order Dataset")
missing_values_order = orders_data.isnull().sum()

print(missing_values_order)

"""Disini yang memiliki Missing Values pada product Dataset. kita dapat mengisinya dengan value lainnya, memprediksi atau menghapusnya. Disini saya akan menghapus baris yang memiliki values yang kosong

#### Memeriksa Duplicated Values
"""

#Customewr
print("Data Duplikat pada Customer Dataset")
duplikat_customer = customers_data.duplicated().sum()

print(duplikat_customer)

#Order
print("Data Duplikat pada Order Dataset")
duplikat_order = orders_data.duplicated().sum()

print(duplikat_order)

#Product
print("Data Duplikat pada Product Dataset")
duplikat_product = products_data.duplicated().sum()

print(duplikat_product)

"""###Cleaning Data"""

#Disini saya hanya cleaning dataset products karena hanya dataset ini yang memiliki missing values
products_data = products_data.dropna()

"""## Exploratory Data Analysis"""

#Judul Dashboard
st.title("Business Orders Dashboard")

# 1. 5 kota (state) yang memiliki pesanan (orders) terbanyak
st.header("1. 10 kota (state) yang memiliki pesanan (orders) terbanyak?")

# mengelompokkan kota dan menjumlahkan pesanannya
state_order_counts = customers_data.groupby("customer_state")["customer_id"].count().reset_index()
state_order_counts.columns = ["State", "Number of Orders"]
state_order_counts = state_order_counts.sort_values(by="Number of Orders", ascending=False)

# 2. Berapa total harga pesanan per kategori produk?
st.header("2. Berapa total harga pesanan per kategori produk?")

# mennggabungkan orders_data dan products_data
merged_data = pd.merge(orders_data, products_data, on="product_id", how="left")

# menggelompokkan product percategory product dan menjumlahkan harga pesanannya
category_price_totals = merged_data.groupby("product_category_name")["price"].sum().reset_index()
category_price_totals.columns = ["Product Category", "Total Order Price"]
category_price_totals = category_price_totals.sort_values(by="Total Order Price", ascending=False)

"""##Visualization & Explanatory Analysis

###Pertanyaan 1
"""

# menampilkan 5 kota yang memiliki pesanan terbanyak
st.subheader("Top States by Number of Orders")
st.write(state_order_counts.head(5))

# menampilkan bar chart
fig_state_orders = px.bar(state_order_counts, x="State", y="Number of Orders",
                          title="State-wise Number of Orders", color="Number of Orders")
st.plotly_chart(fig_state_orders)

"""### Pertanyaan 2"""

# Menampilkan 10 kategori teratas berdasarkan total harga pesanan
st.subheader("Top 10 Product Categories by Total Order Price")
st.write(category_price_totals.head(10))

# membuat bar chart untuk total harga berdasarkan kategori produk
fig_category_price = px.bar(category_price_totals.head(10), x="Product Category", y="Total Order Price",
                            title="Top 10 Product Categories by Total Order Price", color="Total Order Price")
st.plotly_chart(fig_category_price)

"""##Conclusion

1. 5 kota (state) yang memiliki pesanan (orders) terbanyak secara berturut-urut adalah  

<table>
    <tr>
        <th>Kode State</th>
        <th>Total</th>
    </tr>
    <tr>
        <td>SP</td>
        <td>41,746</td>
    </tr>
    <tr>
        <td>RJ</td>
        <td>12,852</td>
    </tr>
    <tr>
        <td>MG</td>
        <td>11,635</td>
    </tr>
    <tr>
        <td>RS</td>
        <td>5,466</td>
    </tr>
    <tr>
        <td>PR</td>
        <td>5,045</td>
    </tr>
</table>

2. Berapa total harga pesanan per kategori produk?  


<table>
    <tr>
        <th>Kategori</th>
        <th>Total Harga</th>
    </tr>
    <tr>
        <td>beleza_saude</td>
        <td>1,258,681.34</td>
    </tr>
    <tr>
        <td>relogios_presentes</td>
        <td>1,205,005.68</td>
    </tr>
    <tr>
        <td>cama_mesa_banho</td>
        <td>1,036,988.68</td>
    </tr>
    <tr>
        <td>esporte_lazer</td>
        <td>988,048.97</td>
    </tr>
    <tr>
        <td>informatica_acessorios</td>
        <td>911,954.32</td>
    </tr>
    <tr>
        <td>moveis_decoracao</td>
        <td>729,762.49</td>
    </tr>
    <tr>
        <td>cool_stuff</td>
        <td>635,290.85</td>
    </tr>
    <tr>
        <td>utilidades_domesticas</td>
        <td>632,248.66</td>
    </tr>
    <tr>
        <td>automotivo</td>
        <td>592,720.11</td>
    </tr>
    <tr>
        <td>ferramentas_jardim</td>
        <td>485,256.46</td>
    </tr>
</table>
"""

# Commented out IPython magic to ensure Python compatibility.
# Navigate to your project folder in Google Drive
# %cd /content/drive/MyDrive/path_to_your_project

# Generate the requirements.txt
!pipreqs .
