from datetime import datetime


def day_of_week_from_offset_timestamp(offset_timestamp: int):
    if offset_timestamp:
        return datetime.fromtimestamp(offset_timestamp).date().weekday()
