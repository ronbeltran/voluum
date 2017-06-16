import time

from datetime import datetime
from datetime import timedelta

import requests

try:
    from urllib.parse import quote_plus
except ImportError:
    # python 2.7
    from urllib import quote_plus

VOLUUM_EMAIL = 'user@example.com'
VOLUUM_PASSWORD = 'notasecret'


class VoluumException(Exception):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def __str__(self):
        return '{0}: {1}'.format(
            self.status_code, self.text)


def fetch(method, url, sleep_time=1, **kwargs):
    """
    Fetch with retry on fail
    http://docs.python-requests.org/en/master/api/#requests.request
    """
    HTTP_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']

    method = method.strip().upper()

    if method.strip().upper() not in HTTP_METHODS:
        raise ValueError('Invalid Http Method: {}'.format(method))

    resp = requests.request(method, url, **kwargs)

    if 'NUMBER_OF_REQUEST_FOR_IP_EXCEEDED' in resp.text:
        time.sleep(sleep_time)
        resp = fetch(method, url, sleep_time=sleep_time * 2, **kwargs)

    return resp


def build_query_str(columns):
    """
    columns is a list of column name
    columns = ['foo', 'bar', 'baz']
    returns:
    "columns=foo&columns=bar&columns=baz"
    """
    if not isinstance(columns, (list, tuple)):
        return ''
    query_str = map(lambda x: 'columns={}'.format(
                    quote_plus(str(x).encode('utf-8'))), columns)
    return '&'.join(query_str)


def round_time(dt=None, round_to=60):
    """
    Round datetime object to nearest hour
    https://stackoverflow.com/questions/3463930
    Result datetime should be formatted like below
    before sending to Voluum  API
        round_time(self.to_date).strftime('%Y-%m-%dT%H')
    """
    if dt is None:
        dt = datetime.now()

    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + timedelta(0, rounding-seconds, -dt.microsecond)
