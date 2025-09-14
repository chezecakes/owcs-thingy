from datetime import datetime
from zoneinfo import ZoneInfo

def getDateAndTime():
    # Get current time in Toronto
    now_toronto = datetime.now(ZoneInfo("America/Toronto"))

    # Format the output
    formatted_time = now_toronto.strftime("%Y-%m-%d %H:%M:%S %Z%z")

    return formatted_time