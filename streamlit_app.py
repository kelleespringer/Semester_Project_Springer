import time # for simulating a real-time data, time loop                    
import pandas as pd # read csv, df manipulation                               
import streamlit as st # data web application development
import requests
import json

st.set_page_config(
    page_title="US Bureau of Labor Statistics Dashboard",
    page_icon=":tophat:",
    layout="wide",
    initial_sidebar_state='expanded'
)
st.title("US Bureau of Labor Statistics Dashboard")
st.write("Lets look at Total Nonfarm Employment, Unemployment Rate, Civilian Unemployment, and Civilian Labor Force. Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/).")

headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['CES0000000001','LNS14000000', 'LNS11000000', 'LNS13000000'],"startyear":"2023", "endyear":"2024"})
p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)


def process_bls_data(json_data):
    data_list = []

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

    df = pd.DataFrame(data_list)
    return df

df = process_bls_data(json_data)
df

if json_data:
    df = process_bls_data(json_data)

    # Data filter for visualization
    data_filter = st.selectbox("Select Data", ("Total Nonfarm Employment", "Unemployment Rate", "Civilian Unemployment", "Civilian Labor Force"))
    series_map = {
        "Total Nonfarm Employment":'CES0000000001',
        "Unemployment Rate":'LNS14000000',
        "Civilian Unemployment":'LNS11000000',
        "Civilian Labor Force":'LNS13000000'
    }

    filtered_df = df[df['series_id'] == series_map[data_filter]]
    filtered_df['value'] = filtered_df['value'].apply(pd.to_numeric, errors='coerce')