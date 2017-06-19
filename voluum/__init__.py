from .security import Security
from .reports import Reports
from .tracker import Tracker
from .utils import VoluumException

VOLUUM_API = 'https://api.voluum.com'


class Voluum:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.security = None
        self.reports = None
        self.tracker = None
        self.token_json = None
        self.token = None
        self.headers = None

    def login(self):
        self.security = Security(self.email, self.password)
        resp = self.security.get_token()

        if resp.status_code == 200:
            self.token_json = resp.json()
            self.token = self.token_json['token']
            self.reports = Reports(self.token)
            self.tracker = Tracker(self.token)
            self.headers = {'cwauth-token': self.token}
        else:
            raise VoluumException(resp.status_code, resp.text)
