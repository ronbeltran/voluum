import os
import unittest

from voluum.security import Security
from voluum.reports import Reports


class ReportsTestCase(unittest.TestCase):
    def setUp(self):
        self.email = os.environ['VOLUUM_EMAIL']
        self.password = os.environ['VOLUUM_PASSWORD']
        self.security = Security(self.email, self.password)
        self.token = self.security.get_token()['token']
        self.reports = Reports(self.token)

    def test_get_report(self):
        from_date = '2017-05-09T15'
        to_date = '2017-06-09T15'
        group_by = 'campaign'
        filter_query = '111dd346-86c3-416f-ad4d-92f2d9ee4638'
        resp = self.reports.get_report(
            from_date, to_date, group_by, filter_query=filter_query)
        self.assertIsNotNone(resp)
