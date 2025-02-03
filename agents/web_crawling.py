from dotenv import load_dotenv
import os
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig
import google.generativeai as genai


async def main():
    load_dotenv()

    browser_cfg = BrowserConfig(headless=True)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(
            url="https://www.amazon.in/s?k=laptops",
        )
        if result.success:
            GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            prompt = "sort by best rating, and give me the price of the first result"
            res = model.generate_content([{"role": "user", "parts": prompt}])
            # with open("result.txt", "w", encoding="utf-8") as file:
            #     file.write(res.text)
            #     print("Saved to result.txt")
            print(res.text)
            print("Done")
        else:
            print(result.error_message)


if __name__ == "__main__":
    asyncio.run(main())
