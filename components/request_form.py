import json
import os
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from module import yextractor as youtube  # Import the youtube.py script
import requests

def get_coordinates(city_name):
    """Fetch latitude and longitude for a given city name."""
    url = f'https://nominatim.openstreetmap.org/search?city={city_name}&format=json'
    headers = {
        'User-Agent': 'stream/1.0'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon
    else:
        st.error("City not found!")
        return None, None
    
def analyze(video_data_file):
    global hashtag, city, radius, start_date, end_date, max_results, chart_type
    try:

        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())


        lat, lon = None, None
        if city:
            lat, lon = get_coordinates(city)

        youtube.video_info(video_data_file, hashtag, lat, lon, radius, max_results, start_date, end_date)

        return True
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False


def request_form(video_data_file):
    global hashtag, city, radius, start_date, end_date, max_results, chart_type, search_status, progress_bar
    # st.set_page_config(page_title="Social-guard", layout="wide", initial_sidebar_state="expanded")

    if not os.path.exists("files"):
        os.makedirs("files")

    st.title("YouTube Channel Dashboard")

    st.subheader("Fetch YouTube Video and Channel Data")
    with st.form("video_fetch_form"):
        hashtag = st.text_input("Enter a hashtag to search for:")
        city = st.text_input("Enter a city name:")
        radius = st.text_input("Enter search radius (e.g., '50km'):", "50km")
        start_date = st.date_input("Start date", value=datetime(2023, 9, 16))
        end_date = st.date_input("End date", value=datetime(2024, 9, 15))
        max_results = st.number_input("Maximum results to fetch:", min_value=1, max_value=50, value=4)
        chart_type = st.selectbox("Select a chart type", ["Bar", "Line", "Area"])

        with open(os.path.join("files","query.json"), "w") as jsonfile:
            json.dump(
                {
                    "hastag":hashtag,
                    "city":city,
                    "radius":radius,
                    "start_date":str(start_date),
                    "end_date":str(end_date),
                    "max_results":max_results
                },
                jsonfile
            )

        submitted = st.form_submit_button("Search")



    if submitted:  
        return analyze(video_data_file)



