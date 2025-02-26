from dotenv import load_dotenv
import os
import google.generativeai as genai
import mesop as me
import mesop.labs as mel

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-2.0-pro-exp-02-05')

@me.page(path='/', title="Chatbot")
def app():
  mel.chat(transform=transform,title="Gemini Chat")


def transform(input:str , history: list[mel.ChatMessage]):
    response = model.generate_content(input)
    yield response.text