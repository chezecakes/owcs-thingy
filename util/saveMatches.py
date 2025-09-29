import time
import json
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def saveMatches(URL, pageToScrape):
    matches = []
    toJSONPath = Path(__file__).parent.parent / 'data' / 'matches.json'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # scrape webpage for html data
        startTime = time.time()
        await page.goto(URL.format(pageToScrape), wait_until='domcontentloaded') # wait until there are no more network requests on the page
        await page.wait_for_timeout(5000)
        endTime = time.time()
        elapsed = endTime - startTime
        print(f'Page parsed in {elapsed} sec')
        # end scraping