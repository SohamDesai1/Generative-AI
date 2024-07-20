from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st
import PIL.Image

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

model_text = genai.GenerativeModel('gemini-pro')
model_image = genai.GenerativeModel('gemini-pro-vision')

def generate_text(prompt):
    # response = model_text.generate_content(prompt)
    chat = model_text.start_chat(history=[])
    chat.send_message(prompt)
    for message in chat.history:
        res = f'**{message.role}**: {message.parts[0].text}'
        print(res)
    return res 
    

def generate_image(prompt):
    response = model_image.generate_content(prompt)
    return response.text

st.title('Gemini Pro AI ')

text,image = st.tabs(['Text','Image'])

with text:
    prompt = st.text_input('Enter a prompt:')
    if st.button('Generate'):
        response = generate_text(prompt)
        st.write(response)
        
with image: 
    image = st.file_uploader(label='Upload an image',type=['jpg', 'jpeg', 'png'])
    if image:
        st.image(image,width=500)
    if st.button('Generate Text from Image'):
        img = PIL.Image.open(image)
        response = generate_image(img)
        st.write(response)