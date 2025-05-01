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

import altair as alt



filename = "Accountreport.csv"

st.title("Automate")
st.write("Processing")
def load_data():
    # Replace with your actual data-loading logic
    return pd.read_csv("video_data.csv")

# Load the data
df = load_data()
st.write(df)
st.subheader("Social Extracted Data and Meta Data")
st.write(df)

st.write("Processing Video One by One")
video_titles = df['Video Title']
video_Link = df['Video URL']


k=0
Finalaclist=[]
for i,j in zip(video_Link,video_titles):
    file_name = f"{k}.txt"
    content=ts.transcript(i,k)
    k=k+1
    st.write("Video Title")
    st.write(j)
    st.write("**************************************")
    if(content==None):
        Finalaclist.append('Yellow')
        st.write("Yellow")
        continue
    st.write("Video Content")
    st.write(content)
    contentsum=sumz.sumup(content)
    print(i,j,content)
    query = tst.trans(j)
    ns=nx.get_news_list(query)
    if(ns==[]):
        Finalaclist.append('Yellow')
        st.write("Yellow")
        continue

    newssum=sumz.sumup(ns)

    print(ns)
    st.write(len(ns))

    st.write("Related News")
    
    st.write(ns)

    st.subheader("Content After Summarizer")
    st.write("Video Summary")
    st.write(contentsum)
    st.write("News Summary")
    st.write(newssum)
   
    st.subheader("Analysis Status")

    state=idefy.validator(contentsum,newssum)
    Finalaclist.append(state)
    st.write(state)
    print(state)




data={
    'Video Title':video_titles,
    'Video Link':video_Link,
    'Status':Finalaclist
}

df2 = pd.DataFrame(data)

# Specify the file name
st.write("Detail Report ")
st.write(df2)
df2.to_csv(filename, index=False)
    










