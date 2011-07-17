from datetime import datetime, timedelta

def timedelta_to_secs(delta):
    return (delta.days * 24 * 60 * 60) + delta.seconds

def base_datetime(dt):
    return datetime(dt.year, dt.month, dt.day)






