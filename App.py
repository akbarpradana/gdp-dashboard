import streamlit as st
import pandas as pd
import plotly.express as px

# Assuming customers_data is already defined and contains the necessary data

# Mengelompokkan kota (state) dan menghitung jumlah pesanan
state_order_counts = customers_data.groupby("customer_state")["customer_id"].count().reset_index()
state_order_counts.columns = ["State", "Number of Orders"]
state_order_counts = state_order_counts.sort_values(by="Number of Orders", ascending=False)

# Menghitung jumlah total pesanan untuk setiap kota
total_orders = state_order_counts['Number of Orders'].sum()

# Menghitung persentase dan menggabungkan yang kurang dari 2% menjadi "Other"
state_order_counts['Percentage'] = (state_order_counts['Number of Orders'] / total_orders) * 100
state_order_counts['State'] = state_order_counts['State'].where(state_order_counts['Percentage'] >= 1.5, 'Other')

# Mengelompokkan dan menjumlahkan untuk kategori "Other"
state_order_counts_grouped = state_order_counts.groupby('State')['Number of Orders'].sum().reset_index()

# Streamlit UI components for filtering
st.header("1. 5 kota (state) yang memiliki pesanan (orders) terbanyak")

# Checkbox filtering for two specific states
selected_states = st.multiselect(
    "Select States to Filter",
    options=state_order_counts_grouped['State'].unique(),
    default=state_order_counts_grouped['State'].unique()[:2]  # Default to first two states
)

# Slider for filtering the number of orders
min_orders, max_orders = st.slider(
    "Select the range of Number of Orders",
    min_value=int(state_order_counts_grouped['Number of Orders'].min()),
    max_value=int(state_order_counts_grouped['Number of Orders'].max()),
    value=(0, int(state_order_counts_grouped['Number of Orders'].max()))  # Default to full range
)

# Filter the data based on selections
filtered_data = state_order_counts_grouped[
    (state_order_counts_grouped['State'].isin(selected_states)) &
    (state_order_counts_grouped['Number of Orders'].between(min_orders, max_orders))
]

# Display the filtered data
st.subheader("Filtered States by Number of Orders")
st.write(filtered_data)

# Create pie chart for filtered data
fig_pie_chart = px.pie(filtered_data, values="Number of Orders", names="State",
                       title="States Contribution by Number of Orders (Filtered)",
                       hole=0.4, labels={'State':'State', 'Number of Orders':'Number of Orders'},
                       hover_data=["Number of Orders"])

# Display pie chart
st.subheader("Pie Chart: Filtered States by Number of Orders")
st.plotly_chart(fig_pie_chart)
