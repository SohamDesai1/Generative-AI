import os
from dotenv import load_dotenv
from pandasai import SmartDataframe
from langchain_groq import ChatGroq
import pandas as pd
import streamlit as st

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

model = ChatGroq(model_name="llama3-70b-8192", api_key=GROQ_API_KEY)

st.title("Chat with CSV!")

upFile = st.file_uploader("Upload Your CSV",type='csv') 

if upFile is not None:
    data = pd.read_csv(upFile)
    df = SmartDataframe(data, config={"llm": model})
    prompt = st.text_area("Enter the prompt...")
    
    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating output..."):
                st.write(df.chat(prompt))