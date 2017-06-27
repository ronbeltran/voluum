import unittest
from pprint import pprint

import datetime

from voluum.utils import build_query_str
from voluum.utils import round_time
from voluum.utils import slice_date_ranges


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
        dt = datetime.datetime(2017, 12, 31, 23, 44, 59, 1234)
        rounded = round_time(dt, round_to=60*60)
        self.assertEqual(rounded.strftime('%Y-%m-%dT%H'),
                         '2018-01-01T00')

        dt2 = datetime.datetime(2017, 12, 31, 23, 25, 59, 1234)
        rounded2 = round_time(dt2, round_to=60*60)
        self.assertEqual(rounded2.strftime('%Y-%m-%dT%H'),
                         '2017-12-31T23')

    def test_slice_date_ranges_custom_step(self):
        today = datetime.datetime(2017, 6, 27)
        end = today + datetime.timedelta(days=1)
        start = end - datetime.timedelta(days=10)

        dates = slice_date_ranges(start, end, step=3)
        expected_dates = [
            (datetime.datetime(2017, 6, 18, 0, 0), datetime.datetime(2017, 6, 20, 0, 0)),
            (datetime.datetime(2017, 6, 21, 0, 0), datetime.datetime(2017, 6, 23, 0, 0)),
            (datetime.datetime(2017, 6, 24, 0, 0), datetime.datetime(2017, 6, 26, 0, 0)),
            (datetime.datetime(2017, 6, 27, 0, 0), datetime.datetime(2017, 6, 28, 0, 0)),
        ]
        self.assertEqual(expected_dates, dates)

    def test_slice_date_ranges_2(self):
        today = datetime.datetime(2017, 6, 27)
        tomorrow = today + datetime.timedelta(days=1)
        date120 = tomorrow - datetime.timedelta(days=120)

        dates = slice_date_ranges(date120, tomorrow, step=31)
        expected_dates = [
            (datetime.datetime(2017, 2, 28, 0, 0), datetime.datetime(2017, 3, 30, 0, 0)),
            (datetime.datetime(2017, 3, 31, 0, 0), datetime.datetime(2017, 4, 30, 0, 0)),
            (datetime.datetime(2017, 5, 1, 0, 0), datetime.datetime(2017, 5, 31, 0, 0)),
            (datetime.datetime(2017, 6, 1, 0, 0), datetime.datetime(2017, 6, 28, 0, 0)),
        ]
        self.assertEqual(expected_dates, dates)
