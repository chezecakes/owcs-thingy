import json
from pathlib import Path

def getTournamentJSON():
    toJSONPath = Path(__file__).parent.parent / 'data' / 'tournaments.json'

    with open(toJSONPath, 'r') as file:
        data = json.load(file)
    
    return data