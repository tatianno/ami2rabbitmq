import unittest
from datetime import datetime
from ami2rabbitmq.entities import QueueCaller
from ami2rabbitmq.exceptions import InvalidEvent


class QueueCallerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.queue_caller = QueueCaller(
            {
                "Event": "QueueCallerJoin",
                "Privilege": "agent,all",
                "Channel": "SIP/IPEu91w-00000002",
                "ChannelState": "6",
                "ChannelStateDesc": "Up",
                "CallerIDNum": "7340",
                "CallerIDName": "Tatianno",
                "ConnectedLineNum": "<unknown>",
                "ConnectedLineName": "<unknown>",
                "Language": "pt_BR",
                "AccountCode": "1",
                "Context": "macro-filas",
                "Exten": "s",
                "Priority": "10",
                "Uniqueid": "1668187694.3",
                "Linkedid": "1668187694.3",
                "Queue": "Queue_11",
                "Position": "1",
                "Count": "1"
            }
        )
        return super().setUp()
    
    def test_queue_caller_create(self):
        self.assertEqual(self.queue_caller.device, "Queue_11")
        self.assertEqual(self.queue_caller.channel, "SIP/IPEu91w-00000002")
        self.assertEqual(self.queue_caller.state, "6")
        self.assertEqual(self.queue_caller.callerid.num, "7340")
        self.assertEqual(self.queue_caller.callerid.name, "Tatianno")
        self.assertEqual(self.queue_caller.connect_line.num, "<unknown>")
        self.assertEqual(self.queue_caller.connect_line.name, "<unknown>")
        self.assertEqual(self.queue_caller.uniqueid, "1668187694.3")
        self.assertEqual(self.queue_caller.linkedid, "1668187694.3")
        self.assertEqual(type(self.queue_caller.last_update), datetime)
        self.assertEqual(self.queue_caller.position, "1")
        self.assertEqual(self.queue_caller.count, "1")
        self.assertEqual(self.queue_caller.type, 'queue_caller')
        self.assertEqual(self.queue_caller.last_event, 'QueueCallerJoin')
        self.assertEqual(self.queue_caller.get_key(), 'Online:QueueCaller:Queue_11:1668187694.3')
    
    def test_queue_caller_dict(self):
        self.assertDictEqual(
            self.queue_caller.get_dict(),
            {
                'device' : "Queue_11",
                'channel' : "SIP/IPEu91w-00000002",
                'state' : "6",
                'last_update' : self.queue_caller.last_update.strftime('%Y-%m-%d %H:%M:%S'),
                'callerid' : {
                    'num' : "7340",
                    "name" : "Tatianno"
                },
                'connect_line' : {
                    'num' : "<unknown>",
                    "name" : "<unknown>"
                },
                'uniqueid' : "1668187694.3",
                'linkedid' : "1668187694.3",
                'position' : '1',
                'count' : '1',
                'last_event' : 'QueueCallerJoin',
                'type' : 'queue_caller'
            }
        )
    
    def test_queue_caller_str(self):
        self.assertEqual(str(self.queue_caller), 'SIP/IPEu91w-00000002')
    
    def test_queue_caller_invalid_event(self):
        with self.assertRaises(InvalidEvent):
            QueueCaller(
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