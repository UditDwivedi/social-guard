import google.generativeai as genai
# from dotenv import load_dotenv
import os
import streamlit as st
# load_dotenv()

# API_KEY = os.getenv("GOOGLE_API_KEY")
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash')

def ask(query:str) -> str:
    response = model.generate_content(query)
    
    full_text = ''
    for part in response.parts:
        full_text += part.text
    
    return full_text

if __name__ == "__main__":
    print(ask("What is the largest planet? repond in name only"))