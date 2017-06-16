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

        resp = self.tracker.get_affiliate_networks(self.campaign_id)

        self.assertEqual(3, len(resp['affiliateNetworks']))
        nw = resp['affiliateNetworks'][0]
        self.assertEqual('8c5e2e8b-f9e7-4385-a266-7c3de1eb2c44', nw['id'])
        self.assertEqual('Network1', nw['name'])
        self.assertEqual(False, nw['deleted'])

    # @responses.activate
    # def test_get_offers(self):
    #     body = AFFILIATE_NETWORKS_DATA

    #     responses.add(
    #         responses.GET, self.url + '/offer',
    #         content_type='application/json; charset=utf-8',
    #         json=body, status=200)

    #     resp = self.tracker.get_offers(self.campaign_id)

    #     self.assertEqual(3, len(resp['offers']))
        # nw = resp['affiliateNetworks'][0]
        # self.assertEqual('8c5e2e8b-f9e7-4385-a266-7c3de1eb2c44', nw['id'])
        # self.assertEqual('Network1', nw['name'])
        # self.assertEqual(False, nw['deleted'])
