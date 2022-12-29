import unittest
from datetime import datetime
from ami2rabbitmq.entities import Bridge
from ami2rabbitmq.exceptions import InvalidEvent


class BridgeTest(unittest.TestCase):

    def setUp(self) -> None:
        self.bridge = Bridge(
            {
                "Event": "BridgeEnter",
                "Privilege": "call,all",
                "BridgeUniqueid": "15d70f0b-5ad0-4235-a4eb-fca0c29a5797",
                "BridgeType": "basic",
                "BridgeTechnology": "simple_bridge",
                "BridgeCreator": "<unknown>",
                "BridgeName": "<unknown>",
                "BridgeNumChannels": "1",
                "BridgeVideoSourceMode": "none",
                "Channel": "SIP/IP-100-GNHHr-00000003",
                "ChannelState": "6",
                "ChannelStateDesc": "Up",
                "CallerIDNum": "100",
                "CallerIDName": "100",
                "ConnectedLineNum": "7340",
                "ConnectedLineName": "Tatianno",
                "Language": "pt_BR",
                "AccountCode": "",
                "Context": "CONTEXT_1",
                "Exten": "IPEu91w",
                "Priority": "1",
                "Uniqueid": "1668187695.4",
                "Linkedid": "1668187694.3"
            }
        )
        return super().setUp()
    
    def test_bridge_create(self):
        self.assertEqual(self.bridge.id, "15d70f0b-5ad0-4235-a4eb-fca0c29a5797")
        self.assertEqual(self.bridge.device, "SIP/IP-100-GNHHr")
        self.assertEqual(self.bridge.channel, "SIP/IP-100-GNHHr-00000003")
        self.assertEqual(self.bridge.state, "6")
        self.assertEqual(self.bridge.callerid.num, "100")
        self.assertEqual(self.bridge.callerid.name, "100")
        self.assertEqual(self.bridge.connect_line.num, "7340")
        self.assertEqual(self.bridge.connect_line.name, "Tatianno")
        self.assertEqual(self.bridge.uniqueid, "1668187695.4")
        self.assertEqual(self.bridge.linkedid, "1668187694.3")
        self.assertEqual(self.bridge.type, 'bridge')
        self.assertEqual(self.bridge.last_event, 'BridgeEnter')
        self.assertEqual(type(self.bridge.last_update), datetime)
        self.assertEqual(self.bridge.get_key(), 'Online:Bridge:1668187695.4')
    
    def test_bridge_dict(self):
        self.assertDictEqual(
            self.bridge.get_dict(),
            {
                'id' : "15d70f0b-5ad0-4235-a4eb-fca0c29a5797",
                'device' : "SIP/IP-100-GNHHr",
                'channel' : "SIP/IP-100-GNHHr-00000003",
                'state' : "6",
                'last_update' : self.bridge.last_update.strftime('%Y-%m-%d %H:%M:%S'),
                'last_event' : 'BridgeEnter',
                'type' : 'bridge',
                'callerid' : {
                    'num' : "100",
                    "name" : "100"
                },
                'connect_line' : {
                    'num' : "7340",
                    "name" : "Tatianno"
                },
                'uniqueid' : "1668187695.4",
                'linkedid' : "1668187694.3"
            }
        )
    
    def test_bridge_str(self):
        self.assertEqual(str(self.bridge), '15d70f0b-5ad0-4235-a4eb-fca0c29a5797')
    
    def test_brigde_invalid_event(self):
        with self.assertRaises(InvalidEvent):
            Bridge(
                {
                    "Event": "DeviceStateChange",
                    "Privilege": "call,all",
                    "Device": "SIP/IP-100-GNHHr",
                    "State": "INUSE"
                }
            )