from voluum.utils import VoluumException
from voluum.utils import fetch


class Reports:

    def __init__(self, token):
        self.token = token

    def headers(self):
        return {
            'Accept': 'application/json',
            'cwauth-token': self.token,
        }

    def get_campaign(self, campaign_id):
        """
        GET /campaign/{campaignId}
        """
        from . import VOLUUM_API

        url = VOLUUM_API + '/campaign/' + campaign_id

        resp = fetch('GET', url, headers=self.headers())

        if resp.status_code != 200:
            raise VoluumException(resp.status_code, resp.text)

        return resp.json()
