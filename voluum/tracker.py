from voluum.utils import VoluumException
from voluum.utils import fetch


class Tracker:

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

        if resp.status_code not in [200, 404]:
            raise VoluumException(resp.status_code, resp.text)

        return resp.json()

    def get_affiliate_networks(self, include_deleted=None, fields=None):
        """
        GET /affiliate-network
        """
        from . import VOLUUM_API

        url = VOLUUM_API + '/affiliate-network'

        if fields is None:
            fields = ''
        elif isinstance(fields, (str, unicode)):
            fields = fields.strip().split(',')

        params = {
            'fields': fields,
        }

        if include_deleted is not None:
            params.update({'includeDeleted': bool(include_deleted)})

        resp = fetch('GET', url, params=params, headers=self.headers())

        if resp.status_code != 200:
            raise VoluumException(resp.status_code, resp.text)

        return resp.json()

    def get_offers(self, include_deleted=None, fields=None):
        """
        GET /offer
        """
        from . import VOLUUM_API

        url = VOLUUM_API + '/offer'

        if fields is None:
            fields = ''
        elif isinstance(fields, (str, unicode)):
            fields = fields.strip().split(',')

        params = {
            'fields': fields,
        }

        if include_deleted is not None:
            params.update({'includeDeleted': bool(include_deleted)})

        resp = fetch('GET', url, params=params, headers=self.headers())

        if resp.status_code != 200:
            raise VoluumException(resp.status_code, resp.text)

        return resp.json()
