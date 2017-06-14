import unittest

from voluum.utils import build_query_str


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
