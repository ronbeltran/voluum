import os
import unittest

from voluum.security import Security
from voluum.utils import VoluumException


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
        with self.assertRaises(VoluumException):
            resp = self.security2.get_token()
            self.assertIsNotNone(resp)

    def test_get_session(self):
        resp = self.security.get_token()
        self.assertIsNotNone(resp)
        self.assertIn('token', resp)
        self.assertIn('inaugural', resp)
        self.assertIn('expirationTimestamp', resp)

        resp2 = self.security.get_session(resp['token'])
        self.assertIsNotNone(resp2)
        self.assertIn('alive', resp2)
        self.assertTrue(resp2['alive'])

    def test_delete_session(self):
        # create session
        resp = self.security.get_token()
        self.assertIsNotNone(resp)
        self.assertIn('token', resp)
        self.assertIn('inaugural', resp)
        self.assertIn('expirationTimestamp', resp)

        # get session
        resp2 = self.security.get_session(resp['token'])
        self.assertIsNotNone(resp2)
        self.assertIn('alive', resp2)
        self.assertTrue(resp2['alive'])

        # delete session
        resp3 = self.security.delete_session(resp['token'])
        self.assertEqual(resp3, '')

        # verify invalidated session
        resp4 = self.security.get_session(resp['token'])
        self.assertIsNotNone(resp4)
        self.assertIn('alive', resp4)
        self.assertFalse(resp4['alive'])
