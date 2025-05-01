import time
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from module import yextractor as youtube  # Import the youtube.py script
import requests


import altair as alt


# Set page configuration for Page 2
# st.set_page_config(page_title="Channel Metrics", layout="wide")
# st.sidebar.title("Channel Metrics")

st.title("Social Content Report")






# Cache data loading to optimize performance
@st.cache_data
def load_data():
    # Replace with your actual data-loading logic
    df =  pd.read_csv("video_data.csv")
    return df

# Load the data
df = load_data()
st.write(df)

try:
    # Ensure the required columns exist
    if "Published At" not in df.columns or "Views" not in df.columns:
        st.error("The dataset must contain 'Published At' and 'Views' columns.")
    else:
        # Format the Published At as a datetime object
        df["Published At"] = pd.to_datetime(df["Published At"])

        # Multi-select for filtering by channels or other criteria (if applicable)
        channels = st.multiselect("Select Channels", df["Channel Title"].unique(), [])

        # Filter data by selected channels if specified
        if channels:
            df = df[df["Channel Title"].isin(channels)]

        if df.empty:
            st.error("No data available for the selected channels.")
        else:
            # Grouping data by Published At to sum views per date
            plot_data = df.groupby(df["Published At"].dt.date)["Views"].sum().reset_index()
            plot_data["Published At"] = pd.to_datetime(plot_data["Published At"])

            # Create the plot
            chart = (
                alt.Chart(plot_data)
                .mark_line(color="steelblue", size=3)
                .encode(
                    x=alt.X("Published At:T", title="Published At"),
                    y=alt.Y("Views:Q", title="Total Views"),
                    tooltip=["Published At:T", "Views:Q"]
                )
                .properties(
                    width=800,
                    height=400,
                    title="Views Over Time for Published Videos"
                )
            )
            st.altair_chart(chart, use_container_width=True)
except Exception as e:
    st.error(f"An error occurred: {e}")