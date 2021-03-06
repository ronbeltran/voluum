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
                   sort='visits', tz='Etc/GMT', limit=1000, offset=0,
                   **kwargs):
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

        root_url = VOLUUM_API + '/report'

        required_columns = [
            'visits', 'clicks', 'conversions', 'revenue',
            'cost', 'profit', 'cpv', 'ctr', 'cr', 'cv',
            'roi', 'epv', 'epc', 'ap', 'errors',
        ]

        if columns is None:
            columns = required_columns
        else:
            required_columns.extend(columns)
            columns = list(set(required_columns))

        date_ranges = [(from_date, to_date)]

        if (to_date - from_date).days > 31:
            date_ranges = slice_date_ranges(from_date, to_date)
            logger.info('time range too long')

        logger.debug(date_ranges)

        resp_json = None

        for index, dr in enumerate(date_ranges):

            logger.debug('{0}: from {1} to {2}'.format(index, dr[0], dr[1]))

            params = {
                'from': round_time(dr[0]).strftime("%Y-%m-%dT%H:%M:%S"),
                'to': round_time(dr[1]).strftime("%Y-%m-%dT%H:%M:%S"),
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
                url = root_url + '?' + build_query_str(columns)

            logger.debug('url: {}'.format(url))
            logger.debug('params: {}'.format(params))
            logger.debug('headers: {}'.format(self.headers()))
            logger.debug('kwargs: {}'.format(kwargs))

            if kwargs:
                params.update(kwargs)

            resp = fetch('GET', url, params=params, headers=self.headers())

            logger.debug('resp.url: {}'.format(resp.url))

            if resp.status_code == 200:

                if resp_json is None:
                    resp_json = resp.json()
                else:
                    new_resp_json = resp.json()

                    resp_json['rows'] += new_resp_json['rows']
                    resp_json['totalRows'] += new_resp_json['totalRows']

                    old_totals = resp_json['totals']
                    new_totals = new_resp_json['totals']

                    for k, v in old_totals.items():
                        resp_json['totals'][k] = v + new_totals[k]

                logger.debug('totalRows: {}'.format(resp_json['totalRows']))
                logger.debug('totals: {}'.format(resp_json['totals']))
                logger.debug('offset: {}'.format(resp_json['offset']))
                logger.debug('rows: {}'.format(len(resp_json['rows'])))
            else:
                raise VoluumException(resp.status_code, resp.text)

        return resp_json

    def manual_costs(self, payload):
        """
        POST /report/manual-cost
        """
        from . import VOLUUM_API

        url = VOLUUM_API + '/report/manual-cost'
        return fetch('POST', url, data=json.dumps(payload),
                     headers=self.headers())
