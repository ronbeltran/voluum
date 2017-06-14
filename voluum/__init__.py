from .security import Security
from .reports import Reports

VOLUUM_API = 'https://api.voluum.com'


class Voluum:
    def __init__(self, email, password):
        self.email = email
        self._security = Security(email, password)
        self.token = self._security.get_token()
        self._reports = Reports(self.token)
