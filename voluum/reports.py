import json

from voluum.utils import build_query_str
from voluum.utils import fetch


class Reports:

    def __init__(self, token):
        self.token = token

    def headers(self):
        return {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'cwauth-token': self.token,
        }

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

        return fetch('GET', url, params=params, headers=self.headers())

    def manual_costs(self, payload):
        """
        POST /report/manual-cost
        """
        from . import VOLUUM_API

        url = VOLUUM_API + '/report/manual-cost'
        return fetch('POST', url, data=json.dumps(payload),
                     headers=self.headers())
