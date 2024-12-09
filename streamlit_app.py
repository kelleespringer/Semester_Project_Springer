import time # for simulating real-time data, time loop                    
import pandas as pd # read csv, df manipulation                                
import streamlit as st # data web application development
import requests
import json

# Set up Streamlit page config
st.set_page_config(
    page_title="US Bureau of Labor Statistics Dashboard",
    page_icon=":tophat:",
    layout="wide",
    initial_sidebar_state='expanded'
)

# Title of the page
st.title("US Bureau of Labor Statistics Dashboard")
st.write("Let's look at Total Nonfarm Employment, Unemployment Rate, Civilian Unemployment, and Civilian Labor Force.")

# Sidebar for user inputs
st.sidebar.header("User Input Features")

# Year selection in sidebar
selected_year = st.sidebar.selectbox("Select a Year", ("2023", "2024"))

# Data fetching from BLS API
headers = {'Content-type': 'application/json'}
data = json.dumps({
    "seriesid": ['CES0000000001', 'LNS14000000', 'LNS13000000', 'LNS12000000'],
    "startyear": selected_year,
    "endyear": selected_year
})

# Requesting data from the BLS API
p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)

# Process the BLS data into a DataFrame
def process_bls_data(json_data):
    data_list = []

    # Extract data from API response
    for series in json_data.get('Results', {}).get('series', []):
        series_id = series.get('seriesID')
        for entry in series.get('data', []):
            year = entry.get('year')
            period = entry.get('period')
            value = entry.get('value')
            data_list.append({
                'series_id': series_id,
                'year': year,
                'period': period,
                'value': value
            })

    # Return the DataFrame
    df = pd.DataFrame(data_list)
    return df

# Only process if there's data
if json_data:
    df = process_bls_data(json_data)

    # Data filter for visualization
    data_filter = st.selectbox("Select Data", ("Total Nonfarm Employment", "Unemployment Rate", "Civilian Unemployment", "Civilian Labor Force"))
    series_map = {
        "Total Nonfarm Employment": 'CES0000000001',
        "Unemployment Rate": 'LNS14000000',
        "Civilian Unemployment": 'LNS13000000',
        "Civilian Labor Force": 'LNS12000000'
    }

    # Filter DataFrame based on selected data type
    filtered_df = df[df['series_id'] == series_map[data_filter]]
    
    # Convert 'value' column to numeric
    filtered_df['value'] = filtered_df['value'].apply(pd.to_numeric, errors='coerce')  
    
    # Display bar chart and scatter chart
    st.bar_chart(filtered_df.set_index('period')['value'])
    st.line_chart(filtered_df.set_index('period')['value'])
