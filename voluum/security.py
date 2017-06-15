import json

from voluum.utils import VoluumException
from voluum.utils import fetch


class Security:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def headers(self):
        return {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
        }

    def get_token(self):
        """ POST /auth/session """
        from . import VOLUUM_API

        url = VOLUUM_API + '/auth/session'

        data = {
            'email': self.email,
            'password': self.password,
        }

        resp = fetch(
            'POST', url, data=json.dumps(data), headers=self.headers())

        if resp.status_code != 200:
            raise VoluumException(resp.status_code, resp.text)

        return resp.json()

    def get_session(self, token):
        """ GET /auth/session """
        from . import VOLUUM_API

        url = VOLUUM_API + '/auth/session'

        headers = self.headers()
        headers.update({
            'cwauth-token': token,
        })

        resp = fetch('GET', url, headers=headers)

        if resp.status_code != 200:
            raise VoluumException(resp.status_code, resp.text)

        return resp.json()

    def delete_session(self, token):
        """ DELETE /auth/session """
        from . import VOLUUM_API

        url = VOLUUM_API + '/auth/session'

        headers = self.headers()
        headers.update({
            'cwauth-token': token,
        })

        resp = fetch('DELETE', url, headers=headers)

        if resp.status_code != 200:
            raise VoluumException(resp.status_code, resp.text)

        return resp.text
