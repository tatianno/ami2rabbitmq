from ami2rabbitmq.repositories import Endpoints
from ami2rabbitmq.repositories import Queues
from ami2rabbitmq.repositories import QueueMembers
from ami2rabbitmq.repositories import Bridges
from ami2rabbitmq.repositories import QueueCallers


class Pabx():

    def __init__(self):
        self.endpoints = Endpoints()
        self.bridges = Bridges()
        self.queue_callers = QueueCallers()
        self.queues = Queues()
        self.queue_members = QueueMembers()
        self._changed_objects = []
        self._create_events = [
            'DeviceStateChange',
            'QueueMemberStatus'
        ]
        self._bridge_create_events = [
            'BridgeEnter',
            'QueueCallerJoin'
        ]
        self._bridge_delete_events = [
            'BridgeLeave',
            'QueueCallerLeave'
        ]
        self._endpoints_bridges_create_events = [
            'BridgeEnter',
        ]
        self._endpoints_bridges_delete_events = [
            'BridgeLeave',
        ]

    def _queue_state_change_event_update(self, event: dict) -> None:
        self._changed_objects.append(
            self.queues.create(event)
        )
    
    def _endpoint_state_change_event_update(self, event: dict) -> None:
        self._changed_objects.append(
            self.endpoints.create(event)
        )
    
    def _bridge_enter_event_update(self, event: dict) -> None:
        self._changed_objects.append(
            self.bridges.create(event)
        )
    
    def _bridge_leave_event_update(self, event: dict) -> None:
        self._changed_objects.append(
            self.bridges.delete(event)
        )
    
    def _queue_caller_leave_event_update(self, event: dict) -> None:
        self._changed_objects.append(
            self.queue_callers.delete(event)
        )
    
    def _queue_caller_join_event_update(self, event: dict) -> None:
        self._changed_objects.append(
            self.queue_callers.create(event)
        )

    def _device_state_change_event_update(self, event: dict):
        if 'Queue:' in event['Device']:
            self._queue_state_change_event_update(event)

        else:
            self._endpoint_state_change_event_update(event)
            
    def _queue_members_status_event_update(self, event: dict) -> None:
        self._changed_objects.append(
            self.queue_members.create(event)
        )
    
    def _create_events_update(self, event: dict) -> None:
        if event['Event'] == 'DeviceStateChange':
            self._device_state_change_event_update(event)
                
        elif event['Event'] == 'QueueMemberStatus':
            self._queue_members_status_event_update(event)
        
    def _bridge_create_events_update(self, event: dict) -> None:
        if event['Event'] == 'BridgeEnter':
            self._bridge_enter_event_update(event)
        
        elif event['Event'] == 'QueueCallerJoin':
            self._queue_caller_join_event_update(event)
    
    def _bridge_delete_events_update(self, event: dict) -> None:
        if event['Event'] == 'BridgeLeave':
            self._bridge_leave_event_update(event)
        
        elif event['Event'] == 'QueueCallerLeave':
            self._queue_caller_leave_event_update(event)
        
    def get_changed_objects(self) -> list:
        return self._changed_objects

    def clear(self) -> None:
        self.endpoints.clear()
        self.bridges.clear()
        self.queue_callers.clear()
        self.queues.clear()
        self.queue_members.clear()
        self._changed_objects = []

    def update(self, events: list) -> list:
        for event in events:
            if event['Event'] in self._create_events:
                self._create_events_update(event)
            
            elif event['Event'] in self._bridge_create_events:
                self._bridge_create_events_update(event)
            
            elif event['Event'] in self._bridge_delete_events:
                self._bridge_delete_events_update(event)
            
        changed_objects = self.get_changed_objects()
        self.clear()
        return changed_objects