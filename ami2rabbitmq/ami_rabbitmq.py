import sys
from time import sleep
from asterisk.manager import (
    Manager,
    ManagerSocketException,
    ManagerAuthException,
    ManagerException
)
from wrapper_rabbitmq_client import RabbitMQProducer
from ami2rabbitmq.manager import Pabx
from ami2rabbitmq.logs_app import LogsApp


class AMI2RabbitMQ():
    _manager = Manager()
    _pabx = Pabx()
    status = None
    events = [
        'BridgeCreate',
        'BridgeEnter',
        'BridgeLeave',
        'BridgeDestroy',
        'DeviceStateChange',
        'QueueMemberStatus',
        'QueueEntry',
        'QueueCallerLeave',
        'QueueCallerJoin',
        'QueueCallerAbandon'
    ]
    version = '0.2.1'

    def __init__(self, ami_settings: dict, rabbitmq_settings: dict, debug: bool=False) -> None:
        self._logs_app = LogsApp(debug)
        self._rabbitmq_producer = RabbitMQProducer(rabbitmq_settings, self._logs_app)
        self.host = ami_settings['host']
        self.user = ami_settings['user']
        self.password = ami_settings['password']
        self.last_events = []

    def _connect(self) -> None:
        self._manager.connect(self.host)
        self._manager.login(self.user, self.password)
    
    def _disconnect(self) -> None:
        self._manager.close()

    def _handle_shutdown(self, event, manager) -> None:
        pass

    def _handle_event(self, event, manager) -> None:
        self.last_events.append(event.headers)
    
    def _clean(self):
        self.last_events = []
    
    def _update_status(self):
        self.status = self._manager.status()
    
    def _send_change_to_broker(self, change_entities: list) -> None:

        for change_entity in change_entities:
            self._rabbitmq_producer.send(change_entity.get_dict())
    
    def changed_events_exists(self):
        return True if len(self.last_events) != 0 else False

    def update_events(self):
        '''
        The change_entities variable receives a list containing the entities that received state change events.

        Entities can be of the type:

        - Bridge : Call established between two endpoints
        - QueueCaller : Call waiting in a queue
        - Endpoint : Can be an extension or trunk
        - QueueMember : Member of a queue
        - Queue : Service queue

        Entities are available for import:
        
        import from ami2rabbitmq.entities import Bridge, Endpoint, QueueCaller, QueueMember, Queue
        '''
        change_entities = self._pabx.update(self.last_events)
        self._send_change_to_broker(change_entities)

    def run(self):
        self._logs_app.register('Service started')
        self._connect()

        try:
            # connect to the manager
            try:
                
                # register some callbacks
                self._manager.register_event(
                    'Shutdown', 
                    self._handle_shutdown
                )

                for evento in self.events:
                    self._manager.register_event(
                        evento, 
                        self._handle_event
                    )
                
                while True:
                    if self.changed_events_exists():
                        self.update_events()
                        self._clean()

                    self._update_status()
                    sleep(1)

            except ManagerSocketException as e:
                self._logs_app.register("Error connecting to the manager: %s" % e.strerror)
                sys.exit(1)

            except ManagerAuthException as e:
                self._logs_app.register("Error logging in to the manager: %s" % e.strerror)
                sys.exit(1)

            except ManagerException as e:
                self._logs_app.register("Error: %s" % e.strerror)
                sys.exit(1)

        finally:
            # remember to clean up
            self._logs_app.register('Encerrando conexões com o Manager')
            self._disconnect()