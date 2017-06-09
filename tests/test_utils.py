import unittest

from voluum.utils import build_columns_query_str


class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        self.columns = ['visits', 'clicks', 'conversions']

    def test_build_columns_query_str(self):
        result = build_columns_query_str(self.columns)
        final_result = 'columns=visits&columns=clicks&columns=conversions'
        self.assertEqual(result, final_result)
