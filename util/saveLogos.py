from pathlib import Path
from bs4 import BeautifulSoup
import os
import requests
from urllib.parse import urlparse

def saveLogos(OWTV_URL, tournamentJSON):
    print("Saving OWCS logos...")

    imageLinks = []

    for tournament in tournamentJSON:
        soup = BeautifulSoup(tournament["card_snapshot"]["raw"], 'html.parser')
        imgTags = soup.find_all('img')
        imgSources = [img['src'] for img in imgTags if 'src' in img.attrs]
        imageLinks.extend(imgSources)

    cleanedImageLinks = list(set(imageLinks)) # removes duplicate values by turning the original list into a set, and then back into a list

    for link in cleanedImageLinks:
        fullLink = OWTV_URL.format(link)
        response = requests.get(fullLink)
        imgName = os.path.basename(link)
        imgPath = Path(__file__).parent.parent / 'data' / 'images' / imgName

        if response.status_code == 200:
            with open(imgPath, 'wb') as imgFile:
                imgFile.write(response.content)
            print(f'Saved image: {imgPath}')
        else:
            print(f'Failed to retrieve image from {fullLink}')
