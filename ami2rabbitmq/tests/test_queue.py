import unittest
from datetime import datetime
from ami2rabbitmq.entities import Queue
from ami2rabbitmq.exceptions import InvalidEvent


class QueueTest(unittest.TestCase):

    def setUp(self) -> None:
        self.queue = Queue(
            {
                "Event": "DeviceStateChange",
                "Privilege": "call,all",
                "Device": "Queue:Queue_11",
                "State": "NOT_INUSE"
            }
        )
        return super().setUp()
    
    def test_queue_create(self):
        self.assertEqual(self.queue.device, "Queue_11")
        self.assertEqual(self.queue.state, "NOT_INUSE")
        self.assertEqual(type(self.queue.last_update), datetime)
        self.assertEqual(self.queue.get_key(), 'Online:Queue:Queue_11')
        self.assertEqual(self.queue.type, 'queue')
        self.assertEqual(self.queue.last_event, 'DeviceStateChange')
    
    def test_queue_dict(self):
        self.assertDictEqual(
            self.queue.get_dict(),
            {
                'device' : "Queue_11",
                'state' : "NOT_INUSE",
                'last_update' : self.queue.last_update.strftime('%Y-%m-%d %H:%M:%S'),
                'queue_callers': [],
                'type' : 'queue',
                'last_event' : 'DeviceStateChange'
            }
        )
    
    def test_queue_str(self):
        self.assertEqual(str(self.queue), 'Queue_11')
    
    def test_queue_member_invalid_event(self):
        with self.assertRaises(InvalidEvent):
            Queue(
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