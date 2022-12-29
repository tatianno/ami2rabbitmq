import unittest
from ami2rabbitmq.redis_db import redis_server
from ami2rabbitmq.manager import Pabx


class PabxTest(unittest.TestCase):
    redis_server.flushall()

    def setUp(self) -> None:
        self.pabx = Pabx()
        return super().setUp()

    def test_bridge_create(self):
        changed_bridges = self.pabx.update(
            [
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
            ]
        )
        self.assertEqual(len(changed_bridges), 1)

        for bridge in changed_bridges:
            self.assertTrue(
                redis_server.exists(bridge.get_key())
            )
            self.assertDictEqual(
                bridge.get_dict(),
                redis_server.get(bridge.get_key())
            )

    def test_endpoint_pabx(self):
        changed_endpoints = self.pabx.update(
            [
                {
                    "Event": "DeviceStateChange",
                    "Privilege": "call,all",
                    "Device": "SIP/IP-100-GNHHr",
                    "State": "NOT_INUSE"
                }
            ]
        )
        self.assertEqual(len(changed_endpoints), 1)

        for endpoint in changed_endpoints:
            self.assertTrue(
                redis_server.exists(endpoint.get_key())
            )
            self.assertDictEqual(
                endpoint.get_dict(),
                redis_server.get(endpoint.get_key())
            )
    
    def test_queue_member_pabx(self):
        changed_queue_members = self.pabx.update(
            [
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
            ]
        )
        self.assertEqual(len(changed_queue_members), 1)

        for queue_member in changed_queue_members:
            self.assertTrue(
                redis_server.exists(queue_member.get_key())
            )
            self.assertDictEqual(
                queue_member.get_dict(),
                redis_server.get(queue_member.get_key())
            )

    def test_queue_pabx(self):
        changed_queues = self.pabx.update(
            [
                {
                    "Event": "DeviceStateChange",
                    "Privilege": "call,all",
                    "Device": "Queue:Queue_11",
                    "State": "NOT_INUSE"
                }
            ]
        )
        self.assertEqual(len(changed_queues), 1)

        for queue in changed_queues:
            self.assertTrue(
                redis_server.exists(queue.get_key())
            )
            self.assertDictEqual(
                queue.get_dict(),
                redis_server.get(queue.get_key())
            )

    def test_bridge_delete(self):
        self.assertTrue(
            redis_server.exists(
                'Online:Bridge:1668187695.4'
            )
        )
        self.pabx.update(
            [
                {
                    "Event": "BridgeLeave",
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
            ]
        )
        self.assertFalse(
            redis_server.exists(
                'Online:Bridge:SIP/IP-100-GNHHr-00000003'
            )
        )

    def test_queue_caller_create(self):
        changed_queue_callers = self.pabx.update(
            [
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
            ]
        )
        self.assertEqual(len(changed_queue_callers), 1)

        for queue_caller in changed_queue_callers:
            self.assertTrue(
                redis_server.exists(queue_caller.get_key())
            )
            self.assertDictEqual(
                queue_caller.get_dict(),
                redis_server.get(queue_caller.get_key())
            )
            
    def test_queue_caller_delete(self):
        self.assertTrue(
            redis_server.exists(
                'Online:QueueCaller:Queue_11:1668187694.3'
            )
        )
        self.pabx.update(
            [
                {
                    "Event": "QueueCallerLeave",
                    "Privilege": "agent,all",
                    "Channel": "SIP/IPEu91w-00000002",
                    "ChannelState": "6",
                    "ChannelStateDesc": "Up",
                    "CallerIDNum": "7340",
                    "CallerIDName": "Tatianno",
                    "ConnectedLineNum": "100",
                    "ConnectedLineName": "100",
                    "Language": "pt_BR",
                    "AccountCode": "1",
                    "Context": "macro-filas",
                    "Exten": "s",
                    "Priority": "10",
                    "Uniqueid": "1668187694.3",
                    "Linkedid": "1668187694.3",
                    "Queue": "Queue_11",
                    "Position": "1",
                    "Count": "0"
                }    
            ]
        )
        self.assertFalse(
            redis_server.exists(
                'Online:QueueCaller:Queue_11:SIP/IPEu91w-00000002'
            )
        )
    
    def test_endpoint_queue_relations(self):
        queue_members = self.pabx.update(
            [
                {
                    "Event": "QueueMemberStatus",
                    "Privilege": "agent,all",
                    "Queue": "Queue_11",
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
                },
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
                },
            ]
        )

        self.assertEqual(len(queue_members), 2)
        queue_member = queue_members[0]
        self.assertEqual(queue_member.get_list_queues_key(), 'Online:QueueMember:SIP/IP-100-GNHHr')
        self.assertListEqual(
            redis_server.get('Online:QueueMember:SIP/IP-100-GNHHr'), 
            ['Queue_11', 'Queue_12']
        )