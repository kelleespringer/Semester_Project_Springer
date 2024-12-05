import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

import requests
import json
import pandas as pd

headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['CEU0000000001','LNS14000000', 'LNS11000000', 'LNS13000000'],"startyear":"2023", "endyear":"2024"})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)

print(json_data)

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







