import json
from pathlib import Path

def getTournamentList(flags='abcou'): # flags will act as filters for tourney types: a=OWCS tourneys, b=FaceIt Masters tourneys, c=Community tourneys, o=ongoing tourneys, u=upcoming tourneys
    tournaments = []
    toJSONPath = Path(__file__).parent.parent / 'data' / 'tournaments.json'
    flagToKeyword = {
        'a':'\nOWCS',
        'b':'\nFaceIt',
        'c':'\nCommunity',
        'o':'\nONGOING',
        'u':'\nUPCOMING'
    }

    with open(toJSONPath, 'r') as file:
        data = json.load(file)
    
    for tournament in data:
        if any(flag in flags and keyword in tournament["anchor_text"] for flag, keyword in flagToKeyword.items()):
            tournaments.append(tournament["anchor_text"] + ':' + tournament["link"])

    return tournaments