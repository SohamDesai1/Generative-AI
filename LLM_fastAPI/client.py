import requests
import streamlit as st


def get_res(input_text):
    url = "http://127.0.0.1:8000/ollama/"  
    endpoint = url + input_text
    response = requests.post(endpoint)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return "Error: Failed to fetch response from the server"


st.title("Llama API")
input_text = st.text_input('Enter text here')

if input_text:
    output_res = get_res(input_text)
    st.write(output_res)

