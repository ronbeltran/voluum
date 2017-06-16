import time
import json
from datetime import datetime
from datetime import timedelta
import responses

from voluum.security import Security
from voluum.utils import VoluumException

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
        self.assertIsNotNone(resp)
        self.assertEqual(self.token, resp['token'])
        self.assertEqual(False, resp['inaugural'])
        self.assertIn('expirationTimestamp', resp)

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
            body=VoluumException(401, json.dumps(body)), status=401)

        # get reference to the exception as `excp`
        with self.assertRaises(VoluumException) as excp:
            self.security2.get_token()

        # assert exception contents
        excp_contents = excp.exception
        self.assertEqual(excp_contents.status_code, 401)
        self.assertEqual(excp_contents.text, json.dumps(body))

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
        self.assertIsNotNone(resp)
        self.assertTrue(resp['alive'])
        self.assertEqual(False, resp['inaugural'])
        self.assertIn('expirationTimestamp', resp)
        self.assertIn('time', resp)

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
        self.assertIsNotNone(resp)
        self.assertFalse(resp['alive'])
        self.assertIn('time', resp)

    @responses.activate
    def test_delete_session(self):
        # delete session
        responses.add(
            responses.DELETE, self.voluum_api + '/auth/session',
            content_type='application/json; charset=utf-8',
            body='', status=200)

        resp = self.security.delete_session(self.token)
        self.assertEqual(resp, '')

    @responses.activate
    def test_delete_session_with_expired_token(self):
        # delete session
        responses.add(
            responses.DELETE, self.voluum_api + '/auth/session',
            content_type='application/json; charset=utf-8',
            body=VoluumException(400, ''), status=400)

        # get reference to the exception as `excp`
        with self.assertRaises(VoluumException) as excp:
            self.security.delete_session(self.token)

        # assert exception contents
        excp_contents = excp.exception
        self.assertEqual(excp_contents.status_code, 400)
        self.assertEqual(excp_contents.text, '')
