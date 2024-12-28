import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

deployment_name = "gpt-4"

prompt = "give me a summary of the movie 'The Matrix'"
response = client.chat.completions.create(
    model=deployment_name,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=50,
)
print(response.choices[0].message.content)
