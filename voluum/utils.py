from datetime import datetime
from datetime import timedelta

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
    """
    if dt is None:
        dt = datetime.now()

    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + timedelta(0, rounding-seconds, -dt.microsecond)
