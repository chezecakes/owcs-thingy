import re

def extractFromCard(card_html):
    # fallback extractor: get text segments and try to parse title/date/status
    text = re.sub(r'\s+', ' ', card_html).strip()
    return {"raw": text}