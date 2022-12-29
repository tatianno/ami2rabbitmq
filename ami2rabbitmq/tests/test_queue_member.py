import unittest
from datetime import datetime
from ami2rabbitmq.entities import QueueMember
from ami2rabbitmq.exceptions import InvalidEvent


class QueueMemberTest(unittest.TestCase):

    def setUp(self) -> None:
        self.queue_member = QueueMember(
            {
                "Event": "QueueMemberStatus",
                "Privilege": "agent,all",
                "Queue": "Queue_12",
                "MemberName": "SIP/IP-100-GNHHr",
                "Interface": "SIP/IP-100-GNHHr",
                "StateInterface": "SIP/IP-100-GNHHr",
                "Membership": "static",
                "Penalty": "0",
                "CallsTaken": "0",
                "LastCall": "0",
                "InCall": "0",
                "Status": "6",
                "Paused": "0",
                "PausedReason": "",
                "Ringinuse": "0"
            }
        )
        return super().setUp()

    def test_queue_member_create(self):
        self.assertEqual(self.queue_member.queue, "Queue_12")
        self.assertEqual(self.queue_member.member_name, "SIP/IP-100-GNHHr")
        self.assertEqual(self.queue_member.interface, "SIP/IP-100-GNHHr")
        self.assertEqual(self.queue_member.state_interface, "SIP/IP-100-GNHHr")
        self.assertEqual(type(self.queue_member.last_update), datetime)
        self.assertEqual(self.queue_member.member_ship, "static")
        self.assertEqual(self.queue_member.penalty, "0")
        self.assertEqual(self.queue_member.calls_taken, "0")
        self.assertEqual(self.queue_member.last_call, "0")
        self.assertEqual(self.queue_member.in_call, "0")
        self.assertEqual(self.queue_member.status, "6")
        self.assertEqual(self.queue_member.paused, "0")
        self.assertEqual(self.queue_member.paused_reason, "")
        self.assertEqual(self.queue_member.ring_inuse, "0")
        self.assertEqual(self.queue_member.type, 'queue_member')
        self.assertEqual(self.queue_member.last_event, 'QueueMemberStatus')
        self.assertEqual(self.queue_member.get_key(), 'Online:QueueMember:SIP/IP-100-GNHHr:Queue_12')
    
    def test_queue_member_dict(self):
        self.assertDictEqual(
            self.queue_member.get_dict(),
            {
                'queue' : 'Queue_12',
                'member_name' : "SIP/IP-100-GNHHr",
                'interface' : "SIP/IP-100-GNHHr",
                'state_interface' : "SIP/IP-100-GNHHr",
                'member_ship' : "static",
                'penalty' : "0",
                'calls_taken' : "0",
                'last_call' : "0",
                'in_call' : "0",
                'status' : "6",
                'paused' : "0",
                'paused_reason' : "",
                'ring_inuse' : "0",
                'last_update' : self.queue_member.last_update.strftime('%Y-%m-%d %H:%M:%S'),
                'last_event' : 'QueueMemberStatus',
                'type' : 'queue_member'
            }
        )
    
    def test_queue_member_str(self):
        self.assertEqual(str(self.queue_member), 'SIP/IP-100-GNHHr:Queue_12')
    
    def test_queue_member_invalid_event(self):
        with self.assertRaises(InvalidEvent):
            QueueMember(
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