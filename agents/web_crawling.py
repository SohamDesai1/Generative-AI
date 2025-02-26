import json
from dotenv import load_dotenv
import os
import asyncio
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)
import google.generativeai as genai


async def main():
    load_dotenv()

    browser_cfg = BrowserConfig(headless=True)
    llm_strategy = LLMExtractionStrategy(
        provider="ollama/llama3.2",
        extraction_type="schema",
        instruction="Extract symbols of all companies.",
        input_format="html",
        verbose=True,
    )
    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy, cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(
            url="https://finance.yahoo.com/quote/%5ENSEI/components/",
            config=crawl_config,
        )
        if result.success:
            data = json.loads(result.extracted_content)
            print("Extracted items:", data)
            print("Done")
        else:
            print(result.error_message)


if __name__ == "__main__":
    asyncio.run(main())
