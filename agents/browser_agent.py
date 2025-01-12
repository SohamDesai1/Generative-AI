import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import SecretStr
import asyncio

load_dotenv()

llm2 = ChatGoogleGenerativeAI(
    api_key=SecretStr(os.getenv("GOOGLE_API_KEY")),
    model="gemini-2.0-flash-exp"   
)

agent = Agent(
    task="Go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result",
    llm=llm2,
    generate_gif=False
)


async def main():
    await agent.run()


asyncio.run(main())
