from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import ollama
from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="LLM API",
    description="LLM API",
    version="0.1.0",
)

prompt=ChatPromptTemplate.from_template("Write me an poem about {topic} for a 5 years child with 100 words")

@app.get("/")
async def root():
    return{"message":"Hello World!"}

@app.post("/ollama/{input_text}")
async def root(input_text:str):
    llm=ollama.ChatOllama(model="llama2")
    chain=prompt|llm
    return{"response":chain.invoke({"topic":input_text})}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
