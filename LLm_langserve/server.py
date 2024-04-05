from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
from langchain.chat_models import ollama
from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="LLM API",
    description="LLM API",
    version="0.1.0",
)

llm=ollama.ChatOllama(model="llama2")

prompt=ChatPromptTemplate.from_template("Write me an essay about {topic} for a 5 years child with 100 words")

add_routes(app,prompt|llm,path="/chat")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)