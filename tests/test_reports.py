from datetime import datetime
from datetime import timedelta

import unittest
import responses

from voluum.reports import Reports
from voluum import VOLUUM_API
from voluum.utils import round_time

REPORT_DATA = {
    "limit": 1,
    "offset": 0,
    "truncated": False,
    "messages": [],
    "totalRows": 1,
    "totals": {
        "advertiserCost": 0,
        "ap": 30.8419,
        "bids": 0,
        "clicks": 3196,
        "conversions": 21,
        "cost": 715.98492,
        "cpv": 0.09288,
        "cr": 0.65707,
        "ctr": 41.45804,
        "cv": 0.27241,
        "epc": 0.20265,
        "epv": 0.08402,
        "errors": 0,
        "ictr": 0,
        "impressions": 0,
        "profit": -68.30492,
        "revenue": 647.68,
        "roi": -9.53999,
        "visits": 7709,
        "winRate": 0
    },
    "rows": [
        {
            "biddingStatus": "ACTIVE",
            "campaignCountry": "United States",
            "campaignId": "2213facf-7ebb-42b1-b1c5-eea60c5f9076",
            "campaignName": "My Campaign",
            # more keys are truncated for brevity
        },
    ]
}


class ReportsTestCase(unittest.TestCase):
    def setUp(self):
        self.url = VOLUUM_API
        self.token = "zZ4J8z6Z5EC5lDDDEAxgnw_kb_qWgkxQ"
        self.reports = Reports(self.token)
        self.from_date = datetime.now() - timedelta(hours=24)
        self.to_date = datetime.now()
        self.campaign_id = '2213facf-7ebb-42b1-b1c5-eea60c5f9076'

    @responses.activate
    def test_get_report(self):
        body = REPORT_DATA

        responses.add(
            responses.GET, self.url + '/report',
            content_type='application/json; charset=utf-8',
            json=body, status=200)

        group_by = 'campaign'
        filter_query = self.campaign_id
        resp = self.reports.get_report(
            round_time(self.from_date).strftime('%Y-%m-%dT%H'),
            round_time(self.to_date).strftime('%Y-%m-%dT%H'),
            group_by, filter_query=filter_query)

        self.assertEqual(1, resp['totalRows'])
        row = resp['rows'][0]
        self.assertEqual(self.campaign_id, row['campaignId'])
        self.assertEqual('My Campaign', row['campaignName'])
        self.assertEqual('ACTIVE', row['biddingStatus'])
