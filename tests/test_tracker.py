import json
import responses

from . import BaseTestCase
from voluum.tracker import Tracker


class TrackerTestCase(BaseTestCase):

    def setUp(self):
        super(TrackerTestCase, self).setUp()
        self.tracker = Tracker(self.token)

    @responses.activate
    def test_get_affiliate_networks(self):
        body = json.loads(self.read_file('affiliateNetworks.json'))

        responses.add(
            responses.GET, self.voluum_api + '/affiliate-network',
            content_type='application/json; charset=utf-8',
            json=body, status=200)

        resp = self.tracker.get_affiliate_networks()

        self.assertEqual(3, len(resp['affiliateNetworks']))
        nw = resp['affiliateNetworks'][0]
        self.assertEqual('8c5e2e8b-f9e7-4385-a266-7c3de1eb2c44', nw['id'])
        self.assertEqual('Network1', nw['name'])
        self.assertEqual(False, nw['deleted'])

    @responses.activate
    def test_get_offers(self):
        body = json.loads(self.read_file('get_offers.json'))

        responses.add(
            responses.GET, self.voluum_api + '/offer',
            content_type='application/json; charset=utf-8',
            json=body, status=200)

        resp = self.tracker.get_offers()

        self.assertEqual(2, len(resp['offers']))
        offer1 = resp['offers'][0]
        offer2 = resp['offers'][1]
        self.assertEqual('30b618d1-44fb-4455-91f5-3caeb309c17f', offer1['id'])
        self.assertEqual('Offer 1', offer1['name'])
        self.assertEqual('5af74826-b69f-444c-90a4-3d411e966355', offer2['id'])
        self.assertEqual('Offer 2', offer2['name'])

    @responses.activate
    def test_get_campaign(self):
        body = json.loads(self.read_file('get_campaign.json'))
        body['id'] = self.campaign_id  # patch campaign_id

        responses.add(
            responses.GET, self.voluum_api + '/campaign/' + self.campaign_id,
            content_type='application/json; charset=utf-8',
            json=body, status=200)

        resp = self.tracker.get_campaign(self.campaign_id)

        self.assertEqual(self.campaign_id, resp['id'])
        self.assertEqual('Campaign Name', resp['name'])
