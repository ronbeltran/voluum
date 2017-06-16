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

        return fetch('GET', url, headers=self.headers())

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

        return fetch('GET', url, params=params, headers=self.headers())

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

        return fetch('GET', url, params=params, headers=self.headers())
