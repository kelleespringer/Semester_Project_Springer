import time
import pandas as pd
import streamlit as st
import requests
import json
import os

st.set_page_config(
    page_title="US Bureau of Labor Statistics Dashboard",
    page_icon=":tophat:",
    layout="wide",
    initial_sidebar_state='expanded'
)

st.title("US Bureau of Labor Statistics Dashboard")
st.write("Let's look at Total Nonfarm Employment, Unemployment Rate, Civilian Unemployment, and Civilian Employment.")

# Sidebar for year selection
st.sidebar.header("Select a Year")
selected_year = st.sidebar.selectbox("Select a Year", ("2019", "2020", "2021", "2022", "2023", "2024"))


headers = {'Content-type': 'application/json'}
data = json.dumps({
    "seriesid": ['CES0000000001', 'LNS14000000', 'LNS13000000', 'LNS12000000'],
    "startyear": selected_year,
    "endyear": selected_year
})

data_directory = 'data/'
csv_file_path = os.path.join(data_directory, 'bls_data.csv')


if not os.path.exists(data_directory):
    os.makedirs(data_directory)

def process_bls_data(json_data):
    data_list = []
    for series in json_data.get('Results', {}).get('series', []):
        series_id = series.get('seriesID')
        data_entries = series.get('data', [])
        if not data_entries:
            continue
        for entry in data_entries:
            year = entry.get('year')
            period = entry.get('period')
            value = entry.get('value')
            data_list.append({
                'series_id': series_id,
                'year': year,
                'period': period,
                'value': value
            })

    df = pd.DataFrame(data_list)
    return df

def fetch_and_save_data():
    p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    df = process_bls_data(json_data)
    df.to_csv(csv_file_path, index=False)
    return df

def load_data_from_csv():
    if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
        try:
            df = pd.read_csv(csv_file_path)
            st.write("Data loaded from CSV file.")
            return df
        except pd.errors.EmptyDataError:
            st.warning("CSV is empty. Fetching new data from the API.")
            return None
    else:
        st.warning("CSV file not found or is empty. Fetching new data from the API.")
        return None

df = load_data_from_csv()

if df is None:
    df = fetch_and_save_data()

data_filter = st.selectbox("Select Data", ("Total Nonfarm Employment", "Unemployment Rate", "Civilian Unemployment", "Civilian Employment"))

series_map = {
    "Total Nonfarm Employment": 'CES0000000001',
    "Unemployment Rate": 'LNS14000000',
    "Civilian Unemployment": 'LNS13000000',
    "Civilian Employment": 'LNS12000000'
}

filtered_df = df[df['series_id'] == series_map[data_filter]]

filtered_df['value'] = filtered_df['value'].apply(pd.to_numeric, errors='coerce')

st.bar_chart(filtered_df.set_index('period')['value'])
st.line_chart(filtered_df.set_index('period')['value'])
