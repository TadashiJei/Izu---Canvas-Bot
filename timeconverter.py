from datetime import datetime, timedelta
from dateutil import tz
from typing import Optional

def timeconverter(date_time: Optional[str]) -> str:
    if date_time is None:
        return "No Date"
    try:
        to_zone = tz.tzlocal()
        UTC = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%SZ')
        central = UTC.astimezone(to_zone)
        offset = int(central.strftime('%z')[:-2])
        dt = datetime(UTC.year, UTC.month, UTC.day, UTC.hour, UTC.minute, UTC.second)
        return str(dt + timedelta(hours=offset))
    except ValueError:
        return "Invalid Date Format"

def time_to_word(timestr: str) -> str:
    if "No" in timestr:
        return "No Date"
    try:
        dt = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%B %d %I:%M %p")
    except ValueError:
        return "Invalid Date Format"