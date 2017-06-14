import unittest

from datetime import datetime

from voluum.utils import build_query_str
from voluum.utils import round_time


class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        self.columns = ['visits', 'clicks', 'conversions']

    def test_build_query_str(self):
        result = build_query_str(self.columns)
        final_result = 'columns=visits&columns=clicks&columns=conversions'
        self.assertEqual(result, final_result)

    def test_build_query_str_invalid_values(self):
        result = build_query_str(None)
        self.assertEqual(result, '')
        result = build_query_str(True)
        self.assertEqual(result, '')
        result = build_query_str([1, True, {}])
        self.assertIsNotNone(result)

    def test_round_time_by_hour(self):
        dt = datetime(2017, 12, 31, 23, 44, 59, 1234)
        rounded = round_time(dt, round_to=60*60)
        self.assertEqual(rounded.strftime('%Y-%m-%d %H:%M:%S'),
                         '2018-01-01 00:00:00')

        dt2 = datetime(2017, 12, 31, 23, 25, 59, 1234)
        rounded2 = round_time(dt2, round_to=60*60)
        self.assertEqual(rounded2.strftime('%Y-%m-%d %H:%M:%S'),
                         '2017-12-31 23:00:00')
