import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Unemployment_Rate_upto_11_2020.csv")
    df = df.rename(columns={'Region': 'State', 'Region.1': 'Location'})
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year

    month_map = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    df['Month_Name'] = df['Month'].apply(lambda x: month_map.get(x, 'Invalid Month'))
    
    return df

df = load_data()

# Sidebar Filters
st.sidebar.title("Filters")
selected_state = st.sidebar.selectbox("Select State", ["All"] + list(df["State"].unique()))
selected_month = st.sidebar.selectbox("Select Month", ["All"] + list(df["Month_Name"].unique()))

# Filter Data
filtered_df = df.copy()
if selected_state != "All":
    filtered_df = filtered_df[filtered_df["State"] == selected_state]
if selected_month != "All":
    filtered_df = filtered_df[filtered_df["Month_Name"] == selected_month]

# App Title
st.title("📊 Unemployment Analysis in India")

# Data Preview
st.subheader("Dataset Overview")
st.write(filtered_df.head())

# Unemployment Rate Trends
st.subheader("📈 Monthly Unemployment Rate")
fig = px.line(filtered_df, x='Date', y='Estimated Unemployment Rate (%)', color='State', title="Unemployment Trends Over Time")
st.plotly_chart(fig)

# Bar Plot of Unemployment Rate
st.subheader("📊 Average Unemployment Rate by State")
df_unemployed = df.groupby('State')['Estimated Unemployment Rate (%)'].mean().reset_index()
fig = px.bar(df_unemployed, x='State', y='Estimated Unemployment Rate (%)', color='State', title='Average Unemployment Rate in Each State')
st.plotly_chart(fig)

# Scatter Plot
st.subheader("🌍 Geographical Unemployment Distribution")
fig = px.scatter_geo(df, lat="Latitude", lon="Longitude", color="State",
                     size="Estimated Unemployment Rate (%)", hover_name="State",
                     title="Impact of Lockdown on Employment across Regions", scope="asia")
st.plotly_chart(fig)

# Insights
st.subheader("📌 Insights")
st.markdown("""
- **Haryana** has the highest unemployment rate.
- **Meghalaya** has the lowest unemployment rate.
- The highest unemployment rates were recorded in **April & May 2020**, during the COVID-19 lockdown.
- The northern regions of India faced the most unemployment.
""")

# Footer
st.markdown("---")
st.write("Built with ❤️ using Streamlit")

