import csv
import os
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from module import yextractor as youtube  # Import the youtube.py script
import requests
from module import nextractor as nx
import pandas as pd

from module import transcribe as ts

from module import summarize as sumz

from module import translate as tst

from module import identifier as idefy

def load_data(file_path):
    return pd.read_csv(file_path)


def content_forensics(video_data_file, forensic_data_file, account_report_file):

    video_data = load_data(video_data_file)        

    st.subheader("Social Extracted Data and Meta Data")
    st.write(video_data)

    st.subheader("Processing Video One by One")
    video_titles = video_data['Video Title']
    video_Link = video_data['Video URL']

    if not os.path.exists(forensic_data_file):
        with open(forensic_data_file, mode='w', newline='', encoding='utf-8') as csvfile:
            field_names = ['Video Title', 'Audio', 'Content', 'ContentSum', 'Translate','News', 'Validate']
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()

            for video_title in video_titles:
                writer.writerow({
                    'Video Title':video_title,
                    'Audio':"pending",
                    'Content':'pending',
                    'ContentSum':"pending",
                    'Translate':'pending',
                    'News':'pending',
                    'Validate':'pending'
                })

    forensic_data = load_data(forensic_data_file)

    k=0
    Finalaclist=[]
    for i,j in zip(video_Link,video_titles):
        print()
        print(f"Processing {j}")
        print()
        audio_path = ""
        if forensic_data.at[k,'Audio'] == 'pending':
            audio_path = ts.download_youtube_audio(i,k)
            forensic_data.at[k,'Audio'] = audio_path
        else:
            audio_path = forensic_data.at[k,'Audio']

        content = ""
        if forensic_data.at[k,'Content'] == 'pending':
            content = ts.transcribe_audio(audio_path)
            forensic_data.at[k,'Content'] = str(content)
        else:
            content = forensic_data.at[k,'Content']
        
        st.write("**************************************")
        st.write("Video Title")
        st.write(j)

        if(content == 'None'):
            Finalaclist.append('Yellow')
            forensic_data.at[k,'ContentSum'] = "No content"
            forensic_data.at[k,'Translate'] = "No content"
            forensic_data.at[k,'News'] = "No content"
            forensic_data.at[k,'Validate'] = "No content"
            forensic_data.to_csv(forensic_data_file,index=False)
            st.write("Yellow")

            continue

        st.write("Video Content")
        st.write(content)
        
        contentsum = ""
        if forensic_data.at[k,'ContentSum'] == 'pending':

            contentsum=sumz.sumup(content)
            forensic_data.at[k,'ContentSum'] = contentsum
        else:
            contentsum = forensic_data.at[k,'ContentSum']

        # print(i,j,content)

        query = ""
        if forensic_data.at[k,'Translate'] == 'pending':
            query=tst.trans(j)
            forensic_data.at[k,'Translate'] = query
        else:
            query = forensic_data.at[k,'Translate']
        
        ns=nx.get_news_list(query)
        # print(ns)
        if(ns==[]):
            Finalaclist.append('Yellow')
            st.write("Yellow")
            continue

        newssum = ""
        if forensic_data.at[k,'News'] == 'pending':
            newssum = sumz.sumup(ns)
            forensic_data.at[k,'News'] = newssum
        else:
            newssum = forensic_data.at[k,'News']


        # st.write("Content After Summarizer")
        st.markdown("### Summary")
        st.write("Video Summary")
        st.write(contentsum)
        st.write("News Summary")
        st.write(newssum)
    
        st.subheader("Analysis Status")

        state = ""
        if forensic_data.at[k,'Validate'] == 'pending':
            state=idefy.validator(contentsum,newssum)
            forensic_data.at[k,'Validate'] = state
        else:
            state = forensic_data.at[k,'Validate']

        Finalaclist.append(state)
        st.write(state)
        # print(state)
        print(forensic_data.iloc[k])
        forensic_data.to_csv(forensic_data_file,index=False)
        k=k+1



    data={
        'Video Title':video_titles,
        'Video Link':video_Link,
        'Status':Finalaclist
    }

    df2 = pd.DataFrame(data)

    # Specify the file name
    st.write("Detail Report")
    st.write(df2)
    df2.to_csv(account_report_file, index=False)
    print("Done\n\n")
            







