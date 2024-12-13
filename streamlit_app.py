import pandas as pd
import streamlit as st
import os
import time

st.set_page_config(
    page_title="US Bureau of Labor Statistics Dashboard",
    page_icon=":tophat:",
    layout="wide",
    initial_sidebar_state='expanded'
)

st.title("US Bureau of Labor Statistics Dashboard")
st.write("Let's look at Total Nonfarm Employment, Unemployment Rate, Civilian Unemployment, and Civilian Employment.")

st.sidebar.header("Select a Year")
selected_year = st.sidebar.selectbox("Select a Year", ("2019", "2020", "2021", "2022", "2023", "2024"))


if os.path.exists("bls_data.csv"):
    df = pd.read_csv("bls_data.csv")
    df_filtered = df[df['year'] == int(selected_year)]
    series_map = {
        "Total Nonfarm Employment": 'CES0000000001',
        "Unemployment Rate": 'LNS14000000',
        "Civilian Unemployment": 'LNS13000000',
        "Civilian Employment": 'LNS12000000'
    }
    data_filter = st.selectbox("Select Data", ("Total Nonfarm Employment", "Unemployment Rate", "Civilian Unemployment", "Civilian Employment"))
    series_id = series_map[data_filter]
    filtered_df = df_filtered[df_filtered['series_id'] == series_id]
    filtered_df['value'] = pd.to_numeric(filtered_df['value'], errors='coerce')

    if filtered_df['value'].isnull().any():
        st.warning("Some values could not be converted to numeric. They have been set to NaN.")

    if not filtered_df.empty:
        st.bar_chart(filtered_df.set_index('period')['value'])
        st.line_chart(filtered_df.set_index('period')['value'])
    else:
        st.write("No data available for the selected filters.")

else:
    st.error("Data file 'bls_data.csv' not found. Please make sure the file is available.")
