import time # for simulating a real-time data, time loop                    
import pandas as pd # read csv, df manipulation                               
import streamlit as st # data web application development

st.set_page_config(
    page_title="US Bureau of Labor Statistics Dashboard",
    page_icon=":tophat:",
    layout="wide",
)
st.title("US Bureau of Labor Statistics Dashboard")
st.write("Lets look at Total Nonfarm Employment, Unemployment Rate, Civilian Unemployment, and Civilian Labor Force. Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/).")

headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['CEU0000000001','LNS14000000', 'LNS11000000', 'LNS13000000'],"startyear":"2023", "endyear":"2024"})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
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

data_filter = st.selectbox("Select Data", ("Total Nonfarm Employment", "Unemployment Rate", "Civilian Unemployment", "Civilian Labor Force"))
df = df[df['series_id'] == data_filter]

#fig_col1, fig_col2, fig_col3, fig_col4 = st.columns(4)
#with fig_col1:
    #import plotly.express as px
    #st.markdown("### Total Nonfarm Employment")
    #fig = px.line(df, x='year', y='value', title=f'{data_filter} Over Time')
    #st.plotly_chart(fig, use_container_width=True)

#with fig_col2:
    #st.markdown("### Unemployment Rate")
    #fig2 = px.line(df, x='year', y='value', title=f'{data_filter} Over Time')
    #st.plotly_chart(fig2, use_container_width=True)

#with fig_col3:
    #st.markdown("### Civilian Unemployment")
    #fig3 = px.line(df, x='year', y='value', title=f'{data_filter} Over Time')
    #st.plotly_chart(fig3, use_container_width=True)

#with fig_col4:
    #st.markdown("### Civilian Labor Force")
    #fig4 = px.line(df, x='year', y='value', title=f'{data_filter} Over Time')
    #st.plotly_chart(fig4, use_container_width=True)
