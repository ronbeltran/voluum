from .security import Security

VOLUUM_API = 'https://api.voluum.com'


class Voluum:
    def __init__(self, email, password):
        self.email = email
        self._security = Security(email, password)
        self.token = self._security.get_token()
