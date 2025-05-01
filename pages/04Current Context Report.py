import streamlit as st
import csv
from module import nextractor as nx
import pandas as pd

from module import translate as tst







st.title("Actual Content Report")

df = pd.read_csv('video_data.csv') 

video_titles = df['Video Title']
video_title_list=[]
newslist=[]
k=0
for i in video_titles:

    print(i)
    st.write("Video Title")
    
    st.write((i))
    query = tst.trans(i)
    ns=nx.get_news_list(query)

    print(ns)
    st.write(len(ns))

    st.write("Related News")
    
    st.write(ns)

    video_title_list.append(i)
    newslist.append(ns)


data={
   'video title':video_title_list,
   'news':newslist
}

#df = pd.DataFrame(data)
#df.to_csv('news_data.csv', index=False)



     

