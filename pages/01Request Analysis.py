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
    

# Set up Streamlit page configuration
st.set_page_config(page_title="Social-guard", layout="wide", initial_sidebar_state="expanded")

# Sidebar for settings
# st.sidebar.title("Dashboard")

# Main dashboard layout
st.title("YouTube Channel Dashboard")

# YouTube Data Fetching Section
st.subheader("Fetch YouTube Video and Channel Data")
with st.form("video_fetch_form"):
    hashtag = st.text_input("Enter a hashtag to search for:")
    city = st.text_input("Enter a city name:")
    radius = st.text_input("Enter search radius (e.g., '50km'):", "50km")
    start_date = st.date_input("Start date", value=datetime(2023, 9, 16))
    end_date = st.date_input("End date", value=datetime(2024, 9, 15))
    max_results = st.number_input("Maximum results to fetch:", min_value=1, max_value=50, value=10)
    chart_type = st.selectbox("Select a chart type", ["Bar", "Line", "Area"])

    csv_filename = st.text_input("Enter the filename to save data:", "video_data.csv")
    #csv_filename="../report/video_data.csv"
    submitted = st.form_submit_button("Just Fetch Data")
    autox = st.form_submit_button("Complete Analysis")

def analyze():
    global hashtag, city, radius, start_date, end_date, max_results, chart_type
    try:
        # Convert dates to datetime objects
        progress_bar = st.progress(0)

        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())

        # Fetch video data
        progress_bar = st.progress(50)

        lat, lon = None, None
        if city:
            lat, lon = get_coordinates(city)
            if lat and lon:
                st.write(f"Coordinates for {city}: Latitude: {lat}, Longitude: {lon}")
            else:
                st.write("Could not retrieve coordinates.")

        st.write("Fetching video data, please wait...")
        youtube.video_info(hashtag, lat, lon, radius, max_results, start_date, end_date, csv_filename)
        progress_bar = st.progress(100)

        st.success(f"Data fetched and saved to {csv_filename}.")
        return True
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False



if submitted:  
    if analyze():  
        st.switch_page("pages/02Social Content Report.py")
    

if autox:
    if analyze():
        st.switch_page("pages/06Automate.py")

       # st.page("Social Content Report")



