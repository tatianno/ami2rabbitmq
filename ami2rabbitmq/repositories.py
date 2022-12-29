from ami2rabbitmq.entities import (
    Bridge,
    Endpoint,
    QueueCaller,
    QueueMember,
    Queue,
    get_endpoint_key,
    get_queue_key
)
from ami2rabbitmq.redis_db import redis_server
from ami2rabbitmq.exceptions import InvalidEvent


class BaseBridgeRepositorie:

    def __init__(self) -> None:
        self._changed_objects = []
        self._redis_server = redis_server
    
    def clear(self) -> None:
        self._changed_objects = []
    
    def get_entity(self, event: dict):
        raise NotImplementedError()
    
    def create(self, event: dict):
        entity = self.entity_create(event)
        self._changed_objects.append(entity)
        self._redis_server.save(
            entity.get_key(), 
            entity.get_dict()
        )
        return entity
    
    def delete(self, event: dict):
        entity = self.entity_delete(event)
        self._changed_objects.append(entity)
        self._redis_server.delete(
            entity.get_key()
        )
        return entity
        

class BaseEndpointQueueRepositorie:

    def __init__(self) -> None:
        self._redis_server = redis_server
        self._changed_objects = []

    def get_entity(self, event: dict):
        raise NotImplementedError()
    
    def clear(self):
        self._changed_objects = []

    def create(self, event: dict):
        entity = self.get_entity(event)
        self._changed_objects.append(entity)
        redis_server.save(
            entity.get_key(), 
            entity.get_dict()
        )
        return entity


class Bridges(BaseBridgeRepositorie):

    def _get_endpoint_key(self, bridge):
        return get_endpoint_key(bridge.device)
    
    def _get_endpoint_data(self, bridge):
        endpoint_key = self._get_endpoint_key(bridge)

        if self._redis_server.exists(endpoint_key):
            return self._redis_server.get(endpoint_key)
        
        return None

    def _get_entity(self, event: dict) -> Bridge:
        if event['Event'] in ['BridgeEnter', 'BridgeLeave'] :
            return  Bridge(event)
        
        else:
            raise InvalidEvent(f"Event Invalid: {event['Event']}")
    
    def entity_create(self, event: dict) -> Bridge:
        bridge = self._get_entity(event)
        endpoint_data = self._get_endpoint_data(bridge)

        if endpoint_data:
            endpoint_data['bridges'].append(bridge.uniqueid)
            self._redis_server.save(
                self._get_endpoint_key(bridge), 
                endpoint_data
            )
        
        return bridge
    
    def entity_delete(self, event: dict) -> Bridge:
        bridge = self._get_entity(event)
        endpoint_data = self._get_endpoint_data(bridge)

        if endpoint_data:
            endpoint_data['bridges'].remove(bridge.uniqueid)
            self._redis_server.save(
                self._get_endpoint_key(bridge), 
                endpoint_data
            )
        
        return bridge


class Endpoints(BaseEndpointQueueRepositorie):

    def _get_endpoint_bridges(self, endpoint: Endpoint) -> list:
        if self._redis_server.exists(endpoint.get_key()):
            return self._redis_server.get(endpoint.get_key())['bridges']
        
        return []
 
    def _endpoint_create(self, event: dict) -> Endpoint:
        endpoint = Endpoint(event)
        endpoint.bridges = self._get_endpoint_bridges(endpoint)       
        return endpoint
    
    def get_entity(self, event: dict) -> Endpoint:

        if event['Event'] == 'DeviceStateChange':
            if 'Queue:' not in event['Device']:
                return self._endpoint_create(event)
        
        raise InvalidEvent(f"Event Invalid: {event['Event']}")


class QueueCallers(BaseBridgeRepositorie):

    def _get_queue_key(self, queue_caller: QueueCaller):
       return get_queue_key(queue_caller.device)
    
    def _get_queue_data(self, queue_caller: QueueCaller):
        queue_key = self._get_queue_key(queue_caller)

        if self._redis_server.exists(queue_key):
            return self._redis_server.get(queue_key)
        
        return None

    def _get_entity(self, event: dict) -> QueueCaller:
        if event['Event'] in ['QueueCallerJoin', 'QueueCallerLeave']:
            return QueueCaller(event)
        
        else:
            raise InvalidEvent(f"Event Invalid: {event['Event']}")
    
    def entity_create(self, event: dict) -> QueueCaller:
        queue_caller = self._get_entity(event)
        queue_data = self._get_queue_data(queue_caller)

        if queue_data:
            queue_data['queue_callers'].append(queue_caller.uniqueid)
            self._redis_server.save(
                self._get_queue_key(queue_caller), 
                queue_data
            )
        
        return queue_caller
    
    def entity_delete(self, event: dict) -> QueueCaller:
        queue_caller = self._get_entity(event)
        queue_data = self._get_queue_data(queue_caller)

        if queue_data:
            queue_data['queue_callers'].remove(queue_caller.uniqueid)
            self._redis_server.save(
                self._get_queue_key(queue_caller), 
                queue_data
            )
        
        return queue_caller


class QueueMembers(BaseEndpointQueueRepositorie):

    def _get_queues_list(self, queue_member: QueueMember)-> list:
        if self._redis_server.exists(queue_member.get_list_queues_key()):
            return self._redis_server.get(queue_member.get_list_queues_key())

        return []

    def _queue_member_create(self, event: dict) -> QueueMember:
        queue_member = QueueMember(event)
        queue_member.queues_list = self._get_queues_list(queue_member)

        if event['Queue'] not in queue_member.queues_list:
            queue_member.queues_list.append(event['Queue'])
            self._redis_server.save(queue_member.get_list_queues_key(), queue_member.queues_list)

        return queue_member

    def get_entity(self, event: dict) -> QueueMember:
        if event['Event'] == 'QueueMemberStatus':
            return self._queue_member_create(event)
        
        raise InvalidEvent(f"Event Invalid: {event['Event']}")


class Queues(BaseEndpointQueueRepositorie):

    def _get_queue_callers(self, queue: Queue) -> list:
        if self._redis_server.exists(queue.get_key()):
            return self._redis_server.get(queue.get_key())['queue_callers'] 

        return [] 
    
    def _queue_create(self, event: dict) -> Queue:
        queue = Queue(event)
        queue.queue_callers = self._get_queue_callers(queue)
        return queue

    def get_entity(self, event: dict) -> Queue:
        if event['Event'] == 'DeviceStateChange':
            if 'Queue:' in event['Device']:
                return self._queue_create(event)
        
        raise InvalidEvent(f"Event Invalid: {event['Event']}")