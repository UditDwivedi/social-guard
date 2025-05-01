import streamlit as st

import streamlit as st
import csv
from module import nextractor as nx
import pandas as pd

from module import transcribe as ts








st.title("Content Forensic")

df = pd.read_csv('video_data.csv') 

video_titles = df['Video Title']
video_Link = df['Video URL']
k=0
for i,j in zip(video_Link,video_titles):
    file_name = f"{k}.txt"
    content=ts.transcript(i,k)
    k=k+1
    st.write("Video Title")
    st.write(j)
    st.write("**************************************")
    if(content!=None):
        st.write("Video Content")
        st.write(content)
        if(type(content)==str):
            
            with open(file_name, "w", encoding="utf-8") as file:

                file.write(content)
    print(i,j,content)




