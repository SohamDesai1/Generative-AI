from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
def generate_content(prompt):
    response = model.generate_content(prompt)
    return response.text

st.title('Gemini AI Text Generator')
prompt = st.text_input('Enter a prompt:')
if st.button('Generate'):
    response = generate_content(prompt)
    st.write(response)