import urllib 
import re


def is_valid_email(email):
    if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email) != None:
        return 1
    return 0


def mk_valid_ascii_str(str_to_convert):

    if not str_to_convert:
        return str_to_convert
    
    try:
        decoded_str = str_to_convert.encode('ascii')
        urllib.urlencode({'blah':decoded_str})
        return str(decoded_str)
    except UnicodeEncodeError:
        decoded_str = re.sub('[^A-Za-z0-9. ]','',str_to_convert)
        return str(decoded_str)