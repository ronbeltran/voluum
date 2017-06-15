import time

import requests

from voluum.utils import build_query_str
from voluum.utils import VoluumException


class Reports:

    def __init__(self, token):
        self.token = token

    def headers(self):
        return {
            'Accept': 'application/json',
            'cwauth-token': self.token,
        }

    def _fetch(self, method, url, sleep_time=1, **kwargs):
        """
        Fetch with retry on fail
        http://docs.python-requests.org/en/master/api/#requests.request
        """
        HTTP_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']

        method = method.strip().upper()

        if method.strip().upper() not in HTTP_METHODS:
            raise ValueError('Invalid Http Method: {}'.format(method))

        resp = requests.request(method, url, **kwargs)

        if resp.status_code != 200:
            if 'NUMBER_OF_REQUEST_FOR_IP_EXCEEDED' in resp.text:
                time.sleep(sleep_time)
            resp = self._fetch(url, method, sleep_time=sleep_time * 2, **kwargs)

        return resp

    def get_report(self, from_date, to_date, group_by, include='ACTIVE',
                   filter_query='', columns=None, direction='DESC',
                   sort='visits', tz='Etc/GMT', limit=1000, offset=0):
        """
        GET /report

        from_date and to_date should be rounded by the hour

        include:
          - ACTIVE
          - ARCHIVED
          - ALL
          - TRAFFIC
        """
        from . import VOLUUM_API

        url = VOLUUM_API + '/report'

        if columns is None:
            columns = [
                'campaign', 'campaignName', 'visits', 'clicks', 'conversions',
                'revenue', 'cost', 'profit', 'cpv', 'ctr', 'cr', 'cv', 'roi',
                'epv', 'epc', 'ap', 'errors',
            ]

        params = {
            'from': from_date,
            'to': to_date,
            'groupBy': group_by,
            'filter': filter_query,
            'direction': direction,
            'sort': sort,
            'tz': tz,
            'limit': limit,
            'offset': offset,
            'include': include,
        }

        if columns:
            url = url + '?' + build_query_str(columns)

        resp = self._fetch('GET', url, params=params, headers=self.headers())

        if resp.status_code != 200:
            raise VoluumException(resp.status_code, resp.text)

        return resp.json()
