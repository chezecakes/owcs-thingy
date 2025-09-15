import os
from dotenv import load_dotenv

load_dotenv()

def getEmojis():
    EMOJI_STR = os.getenv("EMOJIS")
    return EMOJI_STR.split(',')