import json
import requests


class SecurityException(Exception):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def __str__(self):
        return '{0}: {1}'.format(
            self.status_code, self.text)


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

        resp = requests.post(
            url, data=json.dumps(data), headers=self.headers())

        if resp.status_code != 200:
            raise SecurityException(resp.status_code, resp.text)

        return resp.json()

    def get_session(self, token):
        """ GET /auth/session """
        from . import VOLUUM_API

        url = VOLUUM_API + '/auth/session'

        headers = self.headers()
        headers.update({
            'cwauth-token': token,
        })

        resp = requests.get(url, headers=headers)

        if resp.status_code != 200:
            raise SecurityException(resp.status_code, resp.text)

        return resp.json()

    def delete_session(self, token):
        """ DELETE /auth/session """
        from . import VOLUUM_API

        url = VOLUUM_API + '/auth/session'

        headers = self.headers()
        headers.update({
            'cwauth-token': token,
        })

        resp = requests.delete(url, headers=headers)

        if resp.status_code != 200:
            raise SecurityException(resp.status_code, resp.text)

        return resp.text
