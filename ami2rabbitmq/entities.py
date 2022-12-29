from datetime import datetime
from ami2rabbitmq.utils import endpoint_parse, queue_parse
from ami2rabbitmq.exceptions import InvalidEvent


def get_endpoint_key(device):
    return f'Online:Endpoint:{device}'


def get_queue_key(device):
    return f'Online:Queue:{device}'


class Callerid():

    def __init__(self, num, name):
        self.num = num
        self.name = name

    def get_dict(self):
        return {
            'num' : self.num,
            'name' : self.name
        }


class Bridge():

    def __init__(self, event):
        self._bridge_events = [
            'BridgeEnter', 
            'BridgeLeave',
            'QueueCallerJoin',
            'QueueCallerLeave'
        ]

        if event['Event'] not in self._bridge_events:
            raise InvalidEvent(f"Event Invalid: {event['Event']}")

        self.last_update = datetime.now()
        self.id = event['BridgeUniqueid'] if 'BridgeUniqueid' in event else None
        self.device = endpoint_parse(event['Channel'])
        self.channel = event['Channel']
        self.state = event['ChannelState']
        self.callerid = Callerid(
            event['CallerIDNum'],
            event['CallerIDName']
        )
        self.connect_line = Callerid(
            event['ConnectedLineNum'],
            event['ConnectedLineName']
        )
        self.uniqueid = event['Uniqueid']
        self.linkedid = event['Linkedid']
        self.last_event = event['Event']
        self.type = 'bridge'
    
    def __str__(self):
        return self.id

    def get_key(self):
        return f'Online:Bridge:{self.uniqueid}'
    
    def get_dict(self):
        return {
            'id' : self.id,
            'device' : self.device,
            'channel' : self.channel,
            'state' : self.state,
            'last_event' : self.last_event,
            'last_update' : self.last_update.strftime('%Y-%m-%d %H:%M:%S'),
            'callerid' : self.callerid.get_dict(),
            'connect_line' : self.connect_line.get_dict(),
            'uniqueid' : self.uniqueid,
            'linkedid' : self.linkedid,
            'type' : self.type
        }


class QueueCaller(Bridge):
    
    def __init__(self, event):
        super().__init__(event)
        self.device = event['Queue']
        self.position = event['Position']
        self.count = event['Count']
        self.uniqueid = event['Uniqueid']
        self.linkedid = event['Linkedid']
        self.type = 'queue_caller'
    
    def __str__(self):
        return self.channel

    def get_key(self):
        return f'Online:QueueCaller:{self.device}:{self.uniqueid}'
    
    def get_dict(self):
        queue_caller_dict = super().get_dict()
        del queue_caller_dict['id']
        queue_caller_dict['position'] = self.position
        queue_caller_dict['count'] = self.count
        return queue_caller_dict
   

class Endpoint():

    def __init__(self, event):

        if event['Event'] != 'DeviceStateChange':
            raise InvalidEvent(f"Event Invalid: {event['Event']}")

        self.last_update = datetime.now()
        self.last_event = event['Event']
        self.device = event['Device']
        self.state = event['State']
        self.type = 'endpoint'
        self.bridges = []
    
    def __str__(self):
        return self.device
    
    def get_key(self):
        return get_endpoint_key(self.device)

    def get_dict(self):
        return {
            'device' : self.device,
            'state' : self.state,
            'last_update' : self.last_update.strftime('%Y-%m-%d %H:%M:%S'),
            'last_event' : self.last_event,
            'type' : self.type,
            'bridges' : self.bridges
        }


class QueueMember():

    def __init__(self, event):

        if event['Event'] != 'QueueMemberStatus':
            raise InvalidEvent(f"Event Invalid: {event['Event']}")

        self.last_update = datetime.now()
        self.last_event = event['Event']
        self.queue = event['Queue']
        self.member_name = event['MemberName']
        self.interface = event['Interface']
        self.state_interface = event['StateInterface']
        self.member_ship = event['Membership']
        self.penalty = event['Penalty']
        self.calls_taken = event['CallsTaken']
        self.last_call = event['LastCall']
        self.in_call = event['InCall']
        self.status = event['Status']
        self.paused = event['Paused']
        self.paused_reason = event['PausedReason']
        self.ring_inuse = event['Ringinuse']
        self.queues_list = []
        self.type = 'queue_member'
    
    def __str__(self) -> str:
        return f'{self.member_name}:{self.queue}'

    def get_key(self) -> str:
        return f'Online:QueueMember:{self.member_name}:{self.queue}'
    
    def get_list_queues_key(self) -> str:
        return f'Online:QueueMember:{self.member_name}'
    
    def get_dict(self):
        return {
            'queue' : self.queue,
            'member_name' : self.member_name,
            'interface' : self.interface,
            'state_interface' : self.state_interface,
            'member_ship' : self.member_ship,
            'penalty' : self.penalty,
            'calls_taken' : self.calls_taken,
            'last_call' : self.last_call,
            'in_call' : self.in_call,
            'status' : self.status,
            'paused' : self.paused,
            'paused_reason' : self.paused_reason,
            'ring_inuse' : self.ring_inuse,
            'last_update' : self.last_update.strftime('%Y-%m-%d %H:%M:%S'),
            'last_event' : self.last_event,
            'type' : self.type
        }


class Queue():

    def __init__(self, event):

        if event['Event'] != 'DeviceStateChange':
            raise InvalidEvent(f"Event Invalid: {event['Event']}")

        self.last_update = datetime.now()
        self.device = queue_parse(event['Device'])
        self.state = event['State']
        self.queue_callers = []
        self.last_event = event['Event']
        self.type = 'queue'
    
    def __str__(self):
        return self.device
    
    def get_key(self):
        return get_queue_key(self.device)

    def get_dict(self):
        return {
            'device' : self.device,
            'state' : self.state,
            'last_update' : self.last_update.strftime('%Y-%m-%d %H:%M:%S'),
            'queue_callers' : self.queue_callers,
            'last_event' : self.last_event,
            'type' : self.type
        }