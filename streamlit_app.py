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


if 'Results' in json_data:
    # Extract time series data from the response
    all_data = []
    
    # Iterate over each series in the response
    for series in json_data['Results']['series']:
        series_id = series['seriesID']
        
        # Iterate over each data point in the series
        for item in series['data']:
            all_data.append({
                'series_id': series_id,  # Store the series ID
                'year': item['year'],    # Year
                'period': item['period'], # Period (e.g., month with "M")
                'value': item['value'],   # Value (the data point)
            })
    
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(all_data)
    
    # Fix the date column by removing the 'M' from the 'period' and combining with 'year'
    df['date'] = pd.to_datetime(df['year'].astype(str) + df['period'].str[1:], format='%Y%m')
    
    # Convert the 'value' column to numeric (some values may be missing or invalid)
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    # Display the DataFrame
    print(df)
else:
    print("Error: No data found in the response")


