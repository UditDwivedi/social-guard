import csv
import json
import os
import streamlit as st
import pandas as pd
from module import nextractor
import pandas as pd
from module.transcribe import transcript
from module.translate import translator
from module.summarize import summarize
from module.identifier import validator

def load_data(file_path):
    return pd.read_csv(file_path)


def content_forensics(video_data_file, forensic_data_file, account_report_file):

    video_data = load_data(video_data_file)        

    st.subheader("Social Extracted Data and Meta Data")
    st.write(video_data)

    st.subheader("Processing Video One by One")
    video_titles = video_data['Video Title']
    video_Links = video_data['Video URL']

    if not os.path.exists(forensic_data_file):
        with open(forensic_data_file, mode='w', newline='', encoding='utf-8') as csvfile:
            field_names = ['Video Title', 'ContentTags', 'ContentSum', 'News', 'Validate']
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()

            for video_title in video_titles:
                writer.writerow({
                    'Video Title':video_title,
                    'ContentTags':'pending',
                    'ContentSum':"pending",
                    'News':'pending',
                    'Validate':'pending'
                })

    forensic_data = load_data(forensic_data_file)

    # with open(os.path.join("files","query.json"), "r") as jsonfile:
    #     query:dict = json.load(jsonfile)

    k=-1
    Finalaclist=[]
    last_k = 0
    for video_link, video_title in zip(video_Links,video_titles):


        k = k+1
        print()
        print(f"Processing {k} : {video_title}")
        print()

        if(k-last_k > len(video_titles)/10):
            forensic_data.to_csv(forensic_data_file,index=False)
            last_k = k        
        
        st.write("**************************************")
        st.write("Video Title")
        st.write(video_title)

        if forensic_data.at[k,'Validate'] != 'pending':
            print("Already validated")
            st.markdown("### Summary")
            st.write("Video Summary")
            st.write(forensic_data.at[k,'ContentSum'])
            st.write("News Summary")
            st.write(forensic_data.at[k,'News'])
            st.write(forensic_data.at[k,'Validate'])
            Finalaclist.append(forensic_data.at[k,'Validate'])
            continue
        

        content = transcript(video_link,k)
        print("Got Transcript: ")
        print(content, end="\n")
        if content is not None:
            # translating content in transcription
            content = translator.translate(content)
            print("After translation:")
            print(content, end="\n")
        else:
            content = ""

        st.markdown("### Summary")
        

        if(content.strip() == ''):
            Finalaclist.append('Yellow')
            forensic_data.at[k,'ContentTags'] = "No tags"
            forensic_data.at[k,'ContentSum'] = "No content"
            forensic_data.at[k,'News'] = "No news relevance"
            forensic_data.at[k,'Validate'] = "Yellow"
            # forensic_data.to_csv(forensic_data_file,index=False)
            print("No content")
            st.write("No content")
            st.write("Yellow")

            continue

        contentsum = ""
        contenttags = ""
        if forensic_data.at[k,'ContentSum'] == 'pending':

            contentsumwhole = summarize(video_title +':' + content)
            # print("Content Summay", contentsumwhole, sep="\n") 
            contenttags = forensic_data.at[k,'ContentTags'] = contentsumwhole[0].replace(',',' ')
            contentsum = forensic_data.at[k,'ContentSum'] = contentsumwhole[1]
        else:
            contentsum = forensic_data.at[k,'ContentSum']
            contenttags = forensic_data.at[k,'ContentTags']

        print("Content Summarization")
        print(contenttags)
        print(contentsum)
        st.write("Video Summary")
        st.write(contentsum)
        
        news_list = nextractor.get_news_list(contenttags)
        # print(ns)
        newssum = ""
        if(news_list==[]):
            # Finalaclist.append('Yellow')
            forensic_data.at[k,'News'] = "No news relevance"
            # forensic_data.at[k,'Validate'] = "Yellow"
            # forensic_data.to_csv(forensic_data_file,index=False)
            st.write("News Summary")
            st.write("No relevant News Found, Evaluation Authencity low")
            print("No news")

        else:

            news_whole = " ".join(news.content for news in news_list)
            print("news:")
            print(news_whole)
            print()
            
            if forensic_data.at[k,'News'] == 'pending':
                newssum = summarize(news_whole)[1]
                forensic_data.at[k,'News'] = newssum
            else:
                newssum = forensic_data.at[k,'News']
            print("News Summary:")
            print(newssum)
            print()

            # st.write("Content After Summarizer")
            st.write("News Summary")
            st.write(newssum)
    
        st.subheader("Analysis Status")

        state = ""
        if forensic_data.at[k,'Validate'] == 'pending':
            state = validator(contentsum,newssum)
            if(state[-1] == '\n'):
                state = state[:-1]
            forensic_data.at[k,'Validate'] = state
        else:
            state = forensic_data.at[k,'Validate']

        print(state)
        Finalaclist.append(state)
        st.write(state)
        # print(state)
        # print(forensic_data.iloc[k])
        

    forensic_data.to_csv(forensic_data_file,index=False)



    data={
        'Video Title':video_titles,
        'Video Link':video_Links,
        'Status':Finalaclist
    }
    print(data)
    df2 = pd.DataFrame(data)

    # Specify the file name
    st.write("Detail Report")
    st.write(df2)
    df2.to_csv(account_report_file, index=False)
    print("Done\n\n")
            







