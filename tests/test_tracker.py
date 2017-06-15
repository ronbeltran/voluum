import unittest
import responses

from voluum import VOLUUM_API
from voluum.tracker import Tracker

GET_CAMPAIGN_DATA = {
    "id": "",
    "name": "Campaign Name",
    "namePostfix": "281569:topic-Test Seed",
    "createdTime": "2017-06-15T03:58:55.499Z",
    "updatedTime": "2017-06-15T03:58:55.499Z",
    "deleted": False,
    "url": "",
    "impressionUrl": "",
    "costModel": {
        "type": "CPC",
        "value": 0.04
    },
    "revenueModel": {
        "type": "RPA_AUTO"
    },
    "country": {
        "code": "US",
        "name": "United States"
    },
    "trafficSource": {
        "id": ""
    },
    "redirectTarget": {
        "inlineFlow": {
            "name": "Campaign Name - inline flow",
            "deleted": False,
            "countries": [
                {
                    "code": "US",
                    "name": "United States"
                }
            ],
            "defaultPaths": [
                {
                    "name": "Path 1",
                    "active": True,
                    "weight": 100,
                    "landers": [],
                    "offers": [
                        {
                            "weight": 100,
                            "offer": {
                                "id": "1f02e4eb-9783-444c-ae9a-581877d02781"
                            }
                        }
                    ],
                    "offerRedirectMode": "REGULAR",
                    "realtimeRoutingApiState": "DISABLED"
                }
            ],
            "conditionalPathsGroups": [],
            "defaultOfferRedirectMode": "REGULAR",
            "realtimeRoutingApi": "DISABLED"
        }
    },
    "tags": []
}


AFFILIATE_NETWORKS_DATA = {
    "affiliateNetworks": [
        {
            "id": "8c5e2e8b-f9e7-4385-a266-7c3de1eb2c44",
            "name": "Network1",
            "deleted": False,
        },
        {
            "id": "8c5e2e8b-f9e7-4385-a266-7c3de1eb2c45",
            "name": "Network2",
            "deleted": False,
        },
        {
            "id": "8c5e2e8b-f9e7-4385-a266-7c3de1eb2c46",
            "name": "Network3",
            "deleted": False,
        },
    ]
}


class TrackerTestCase(unittest.TestCase):

    def setUp(self):
        self.url = VOLUUM_API
        self.token = "zZ4J8z6Z5EC5lDDDEAxgnw_kb_qWgkxQ"
        self.campaign_id = '2213facf-7ebb-42b1-b1c5-eea60c5f9076'
        self.tracker = Tracker(self.token)

    @responses.activate
    def test_get_affiliate_networks(self):
        body = AFFILIATE_NETWORKS_DATA

        responses.add(
            responses.GET, self.url + '/affiliate-network',
            content_type='application/json; charset=utf-8',
            json=body, status=200)

        resp = self.tracker.get_affiliate_networks(self.campaign_id)

        self.assertEqual(3, len(resp['affiliateNetworks']))
        nw = resp['affiliateNetworks'][0]
        self.assertEqual('8c5e2e8b-f9e7-4385-a266-7c3de1eb2c44', nw['id'])
        self.assertEqual('Network1', nw['name'])
        self.assertEqual(False, nw['deleted'])
