import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from browser_use import Agent
from pydantic import SecretStr
import asyncio

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment="gpt-4",
    api_key=SecretStr(os.getenv("AZURE_OPENAI_API_KEY")),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    rate_limiter=None,
)

agent = Agent(
    task="Go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result",
    llm=llm,
)


async def main():
    await agent.run(max_steps=3)


asyncio.run(main())
