import os
import unittest

from voluum.security import Security
from voluum.security import SecurityException


class SecurityTestCase(unittest.TestCase):
    def setUp(self):
        self.email = os.environ['VOLUUM_EMAIL']
        self.password = os.environ['VOLUUM_PASSWORD']
        self.security = Security(self.email, self.password)
        self.security2 = Security(self.email, self.password + '_')

    def test_get_token(self):
        resp = self.security.get_token()
        self.assertIsNotNone(resp)
        self.assertIn('token', resp)
        self.assertIn('inaugural', resp)
        self.assertIn('expirationTimestamp', resp)

    def test_get_token_wrong_credentials(self):
        with self.assertRaises(SecurityException):
            resp = self.security2.get_token()
            self.assertIsNotNone(resp)
