import json
from pathlib import Path
from bs4 import BeautifulSoup
import os
import requests
from urllib.parse import urlparse

from getTournamentJSON import getTournamentJSON # for debugging, remove later

def saveLogos(OWTV_URL, tournamentJSON):
    imageLinks = []

    for tournament in tournamentJSON:
        soup = BeautifulSoup(tournament["card_snapshot"]["raw"], 'html.parser')
        imgTags = soup.find_all('img')
        imgSources = [img['src'] for img in imgTags if 'src' in img.attrs]
        imageLinks.extend(imgSources)

    cleanedImageLinks = list(set(imageLinks)) # removes duplicate values by turning the original list into a set, and then back into a list
    print(cleanedImageLinks) # debug

    for link in cleanedImageLinks:
        response = requests.get(OWTV_URL.format(link))

        # if response.status_code == 200:
        #     with open()

saveLogos('https://owtv.gg{}', getTournamentJSON())
