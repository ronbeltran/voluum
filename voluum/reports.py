import json
import logging

from voluum.utils import build_query_str
from voluum.utils import fetch
from voluum.utils import round_time
from voluum.utils import slice_date_ranges
from voluum.utils import VoluumException

logger = logging.getLogger(__name__)


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
        logger.info('reports:get_report()')
        from . import VOLUUM_API

        url = VOLUUM_API + '/report'

        if columns is None:
            columns = [
                'campaign', 'campaignName', 'visits', 'clicks', 'conversions',
                'revenue', 'cost', 'profit', 'cpv', 'ctr', 'cr', 'cv', 'roi',
                'epv', 'epc', 'ap', 'errors',
            ]

        date_ranges = [(from_date, to_date)]

        if (to_date - from_date).days > 31:
            date_ranges = slice_date_ranges(from_date, to_date)
            logger.info('time range too long')

        logger.debug(date_ranges)

        resp_json = None

        for dr in date_ranges:

            params = {
                'from': round_time(dr[0]).strftime('%Y-%m-%dT%H'),
                'to': round_time(dr[1]).strftime('%Y-%m-%dT%H'),
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

            logger.debug(url)
            logger.debug(params)
            resp = fetch('GET', url, params=params, headers=self.headers())

            if resp.status_code == 200:
                if resp_json is None:
                    resp_json = resp.json()
                else:
                    resp_json['rows'] += resp.json()['rows']
            else:
                raise VoluumException(resp.status_code, resp.text)

        logger.debug(resp_json)
        return resp_json

    def manual_costs(self, payload):
        """
        POST /report/manual-cost
        """
        from . import VOLUUM_API

        url = VOLUUM_API + '/report/manual-cost'
        return fetch('POST', url, data=json.dumps(payload),
                     headers=self.headers())
