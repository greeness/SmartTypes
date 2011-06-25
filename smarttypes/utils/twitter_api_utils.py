
from dateutil import tz
from datetime import datetime

HERE = tz.tzlocal()
UTC = tz.tzutc()

def get_rate_limit_status(api_handle):
    rate_limit_status_dict = api_handle.rate_limit_status()
    remaining_hits = rate_limit_status_dict['remaining_hits']
    reset_time_in_seconds = rate_limit_status_dict['reset_time_in_seconds']
    reset_time_utc = datetime.utcfromtimestamp(reset_time_in_seconds)
    reset_time_utc = reset_time_utc.replace(tzinfo=UTC)
    reset_time = reset_time_utc.astimezone(HERE)
    return remaining_hits, reset_time
