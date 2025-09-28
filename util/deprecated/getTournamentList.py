# DEPRECATED AS OF 9/28/2025

import json
from pathlib import Path

def getTournamentList(tournamentJSON, flags='abcou'): # flags will act as filters for tourney types: a=OWCS tourneys, b=FaceIt Masters tourneys, c=Community tourneys, o=ongoing tourneys, u=upcoming tourneys
    tournaments = []
    flagToKeyword = {
        'a':'\nOWCS',
        'b':'\nFaceIt',
        'c':'\nCommunity',
        'o':'\nONGOING',
        'u':'\nUPCOMING'
    }
    
    for tournament in tournamentJSON:
        if any(flag in flags and keyword in tournament["anchor_text"] for flag, keyword in flagToKeyword.items()):
            tournaments.append(tournament["anchor_text"] + ':' + tournament["link"])

    return tournaments