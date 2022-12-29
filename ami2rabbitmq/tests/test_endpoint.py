import unittest
from datetime import datetime
from ami2rabbitmq.entities import Endpoint
from ami2rabbitmq.exceptions import InvalidEvent


class EndPointTest(unittest.TestCase):

    def setUp(self) -> None:
        self.endpoint = Endpoint(
            {
                "Event": "DeviceStateChange",
                "Privilege": "call,all",
                "Device": "SIP/IP-100-GNHHr",
                "State": "NOT_INUSE"
            }
        )
        return super().setUp()

    def test_endpoint_create(self):
        self.assertEqual(self.endpoint.device, "SIP/IP-100-GNHHr")
        self.assertEqual(self.endpoint.state, "NOT_INUSE")
        self.assertEqual(type(self.endpoint.last_update), datetime)
        self.assertEqual(self.endpoint.get_key(), 'Online:Endpoint:SIP/IP-100-GNHHr')
        self.assertEqual(self.endpoint.type, 'endpoint')
        self.assertEqual(self.endpoint.last_event, 'DeviceStateChange')
    
    def test_endpoint_dict(self):
        self.assertDictEqual(
            self.endpoint.get_dict(),
            {
                'device' : "SIP/IP-100-GNHHr",
                'state' : "NOT_INUSE",
                'last_update' : self.endpoint.last_update.strftime('%Y-%m-%d %H:%M:%S'),
                'bridges': [],
                'type' : 'endpoint',
                'last_event' : 'DeviceStateChange'
            }
        )
    
    def test_endpoint_str(self):
        self.assertEqual(str(self.endpoint), 'SIP/IP-100-GNHHr')
    
    def test_endpoint_invalid_event(self):
        with self.assertRaises(InvalidEvent):
            Endpoint(
                {
                    "Event": "BridgeCreate",
                    "Privilege": "call,all",
                    "BridgeUniqueid": "b277e630-8273-4c5a-a582-de47213e0fe1",
                    "BridgeType": "basic",
                    "BridgeTechnology": "simple_bridge",
                    "BridgeCreator": "<unknown>",
                    "BridgeName": "<unknown>",
                    "BridgeNumChannels": "0",
                    "BridgeVideoSourceMode": "none"
                }
            )