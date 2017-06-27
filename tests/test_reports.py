import json
from datetime import datetime
from datetime import timedelta

import responses

from voluum.reports import Reports

from . import BaseTestCase


class ReportsTestCase(BaseTestCase):
    def setUp(self):
        super(ReportsTestCase, self).setUp()
        self.reports = Reports(self.token)
        self.from_date = datetime.now() - timedelta(hours=24)
        self.to_date = datetime.now()

    @responses.activate
    def test_get_report(self):
        body = json.loads(self.read_file('get_report.json'))

        responses.add(
            responses.GET, self.voluum_api + '/report',
            content_type='application/json; charset=utf-8',
            json=body, status=200)

        group_by = 'campaign'
        filter_query = self.campaign_id

        resp = self.reports.get_report(
            self.from_date, self.to_date,
            group_by, filter_query=filter_query)

        self.assertEqual(1, resp['totalRows'])
        row = resp['rows'][0]
        self.assertEqual(self.campaign_id, row['campaignId'])
        self.assertEqual('My Campaign', row['campaignName'])
        self.assertEqual('ACTIVE', row['biddingStatus'])
