import time
from datetime import datetime
from datetime import timedelta
import responses

from voluum.security import Security

from . import BaseTestCase


class SecurityTestCase(BaseTestCase):
    def setUp(self):
        super(SecurityTestCase, self).setUp()
        self.security = Security(self.email, self.password)
        self.security2 = Security(self.email, self.password + '_')
        self.now = datetime.now() + timedelta(hours=1)

    @responses.activate
    def test_get_token(self):
        body = {
            "token": self.token,
            "expirationTimestamp": self.now.isoformat(),
            "inaugural": False,
        }
        responses.add(
            responses.POST, self.voluum_api + '/auth/session',
            content_type='application/json; charset=utf-8',
            json=body, status=200)

        resp = self.security.get_token()
        r = resp.json()

        self.assertEqual(200, resp.status_code)

        self.assertIsNotNone(r)
        self.assertEqual(self.token, r['token'])
        self.assertEqual(False, r['inaugural'])
        self.assertIn('expirationTimestamp', r)

    @responses.activate
    def test_get_token_wrong_credentials(self):
        body = {
            "error": {
                "code": "BAD_CREDENTIALS",
                "description": "",
                "messages": [],
                "webRequestId": "req-12k-2mA3Abz2So8DtXCf",
                "time": "2017-06-14T04:18:28.549+0000"
            },
            "status": "UNAUTHORIZED",
            "typeName": "badCredentials",
            "typeCode": [
                401,
                0
            ],

        }

        responses.add(
            responses.POST, self.voluum_api + '/auth/session',
            content_type='application/json; charset=utf-8',
            json=body, status=401)

        resp = self.security2.get_token()
        self.assertEqual(resp.status_code, 401)

        r = resp.json()
        error = r['error']
        self.assertEqual('BAD_CREDENTIALS', error['code'])

    @responses.activate
    def test_get_session(self):
        body = {
            "alive": True,
            "expirationTimestamp": self.now.isoformat(),
            "inaugural": False,
            "time": int(time.time()),
        }

        responses.add(
            responses.GET, self.voluum_api + '/auth/session',
            content_type='application/json; charset=utf-8',
            json=body, status=200)

        resp = self.security.get_session(self.token)
        r = resp.json()

        self.assertEqual(200, resp.status_code)
        self.assertIsNotNone(r)
        self.assertTrue(r['alive'])
        self.assertEqual(False, r['inaugural'])
        self.assertIn('expirationTimestamp', r)
        self.assertIn('time', r)

    @responses.activate
    def test_get_session_with_expired_token(self):
        body = {
            "alive": False,
            "time": int(time.time()),
        }

        responses.add(
            responses.GET, self.voluum_api + '/auth/session',
            content_type='application/json; charset=utf-8',
            json=body, status=200)

        resp = self.security.get_session(self.token)
        r = resp.json()

        self.assertEqual(200, resp.status_code)
        self.assertIsNotNone(r)
        self.assertFalse(r['alive'])
        self.assertIn('time', r)

    @responses.activate
    def test_delete_session(self):
        # delete session
        responses.add(
            responses.DELETE, self.voluum_api + '/auth/session',
            content_type='application/json; charset=utf-8',
            body='', status=200)

        resp = self.security.delete_session(self.token)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.text, '')

    @responses.activate
    def test_delete_session_with_expired_token(self):
        # delete session
        responses.add(
            responses.DELETE, self.voluum_api + '/auth/session',
            content_type='application/json; charset=utf-8',
            body='', status=400)

        resp = self.security.delete_session(self.token)
        self.assertEqual(400, resp.status_code)
        self.assertEqual('', resp.text)
