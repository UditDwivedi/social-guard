import streamlit as st
import pandas as pd
from components.request_form import request_form
from components.content_forensics import content_forensics
from components.account_report import account_report
import os

st.set_page_config(page_title="Social Guard", layout="wide")

video_data_file = os.path.join("files","video_data.csv")
forensic_status_file = os.path.join("files","forensic_data.csv")
account_report_file = os.path.join("files","account_report.csv")

if request_form(video_data_file) or os.path.exists(video_data_file):
    content_forensics(video_data_file,forensic_status_file, account_report_file)
    account_report(account_report_file)

    if st.button("Reset"):
        for file in os.listdir("files"):
            os.remove(f"files/{file}")
        
        # for key in st.session_state.keys():
        #     del key

        # st.session_state.clear()

            







