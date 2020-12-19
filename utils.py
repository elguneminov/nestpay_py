import datetime 
import time
import hashlib
import base64

def microtime(get_as_float = False) :
    d = datetime.datetime.now()
    t = time.mktime(d.timetuple())
    if get_as_float:
        return t
    else:
        ms = d.microsecond / 1000000.
        return '%f %d' % (ms, t)


def convert_string_to_hash(word):
    digest = hashlib.sha1(word.encode())
    result = base64.b64encode(digest.digest())
    return result



def substr(string, start, length = None):
    if start < 0:
        start = start + len(string)
    if not length:
        return string[start:]
    elif length > 0:
        return string[start:start + length]
    else:
        return string[start:length]