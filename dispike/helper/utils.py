import datetime
import re


def parse_time(timestamp):
    if timestamp:
        return datetime.datetime(
            *map(int, re.split(r"[^\d]", timestamp.replace("+00:00", "")))
        )
    return None
