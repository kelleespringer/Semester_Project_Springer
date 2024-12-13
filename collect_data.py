import requests
import pandas as pd
import json
import os

# Define the path to the stored CSV file
CSV_FILE_PATH = 'bls_data.csv'

# BLS API request headers and payload
headers = {'Content-type': 'application/json'}

# Function to fetch BLS data for a specific year
def fetch_bls_data(year):
    data = json.dumps({
        "seriesid": ['CES0000000001', 'LNS14000000', 'LNS13000000', 'LNS12000000'],
        "startyear": year,
        "endyear": year
    })

    response = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error fetching data from BLS API: {response.text}")

    return response.json()

# Function to process BLS data into a DataFrame
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

    # Create DataFrame
    df = pd.DataFrame(data_list)
    return df

# Function to append new data to the CSV file
def append_data_to_csv(new_data_df):
    # If the CSV file exists, load it, otherwise create a new one
    if os.path.exists(CSV_FILE_PATH):
        existing_data_df = pd.read_csv(CSV_FILE_PATH)
        # Append the new data to the existing data
        combined_df = pd.concat([existing_data_df, new_data_df]).drop_duplicates(subset=['series_id', 'year', 'period'], keep='last')
        combined_df.to_csv(CSV_FILE_PATH, index=False)
    else:
        # If the CSV doesn't exist, just save the new data
        new_data_df.to_csv(CSV_FILE_PATH, index=False)

# Main function to collect and append data
def main():
    # Get the current year and the previous year
    current_year = '2024'  # For example, set this dynamically if needed
    print(f"Fetching BLS data for {current_year}...")

    # Fetch new BLS data
    json_data = fetch_bls_data(current_year)
    new_data_df = process_bls_data(json_data)

    # Append the new data to the CSV
    append_data_to_csv(new_data_df)
    print("Data has been successfully updated.")

if __name__ == "__main__":
    main()
