import time
import json
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def saveTournaments(URL, pageToScrape):
    tournaments = []
    toJSONPath = Path(__file__).parent.parent / 'data' / 'tournaments.json'

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

        # looks for tournament cards with anchor links to the respective tournament
        anchors = page.locator("a[href*='/tournaments']")
        count = await anchors.count()

        for i in range(count):
            a = anchors.nth(i)
            try:
                href = await a.get_attribute("href") or ""
                textVal = await a.inner_text()
                text = textVal.strip() if textVal else ""
            except Exception:
                href = await a.get_attribute("href") or ""
                textVal = await a.text_content()
                text = textVal.strip() if textVal else ""
            # attempt to pull parent block text (card)
            card = a.locator("xpath=ancestor::div[1]")
            card_html = ""
            try:
                card_html = await card.inner_html()
            except Exception:
                card_html = text
            tournaments.append({
                "link": href,
                "anchor_text": text,
                "card_snapshot": card_html
            })

        await browser.close()

    # post processing: 
    # Remove exact duplicates and the tournament header card (which isn't an actual tournament; it is always the first element)
    # remove card snapshot html that is irrelevant to each card
    # save to files
    unique = { (t.get("link") or t.get("anchor_text")): t for t in tournaments }
    output = list(unique.values())
    del output[0]

    for item in output:
        soup = BeautifulSoup(item['card_snapshot'], 'html.parser')
        matching_a = soup.find('a', href=item['link'])
        if matching_a:
            item['card_snapshot'] = str(matching_a)
        else:
            item['card_snapshot'] = None

    with open(toJSONPath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(output)} items to tournaments.json and raw HTML to OWTV_tournaments.html")