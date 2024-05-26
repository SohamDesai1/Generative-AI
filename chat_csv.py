from pandasai import SmartDataframe
from pandasai.llm.local_llm import LocalLLM
import pandas as pd
import streamlit as st

ollama_llm = LocalLLM(api_base="http://localhost:11434/v1", model="llama3:8b")

st.title("Chat with CSV!")

upFile = st.file_uploader("Upload Your CSV",type='csv') 

if upFile is not None:
    data = pd.read_csv(upFile)
    df = SmartDataframe(data, config={"llm": ollama_llm})
    prompt = st.text_area("Enter the prompt...")
    
    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating output..."):
                st.write(df.chat(prompt))