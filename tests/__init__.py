import os
import unittest

from voluum import VOLUUM_API
from voluum.utils import VOLUUM_EMAIL
from voluum.utils import VOLUUM_PASSWORD

BASE_DIR = os.path.join(os.path.dirname(__file__))
DATA_FILES_DIR = os.path.join(BASE_DIR, 'data')


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.email = VOLUUM_EMAIL
        self.password = VOLUUM_PASSWORD
        self.voluum_api = VOLUUM_API
        self.token = "zZ4J8z6Z5EC5lDDDEAxgnw_kb_qWgkxQ"
        self.campaign_id = '2213facf-7ebb-42b1-b1c5-eea60c5f9076'

    def read_file(self, filename):
        path = os.path.join(DATA_FILES_DIR, filename)
        with open(path, 'r') as f:
            return f.read()
