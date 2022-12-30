# AMI2RabbitMQ

## Overview

Is a consumer of events produced by the Asterisk Manager Interface, where it organizes endpoints, bridges and queues into entities, persisting the last state on a redis server and producing an event for a queue on a RabbitMQ server.

The generated data is persisted on the Redis Server with keys starting with the prefix **Online:**< SUFIX >.

## Dependencies

It is necessary to have Redis, RabbitMQ, Asterisk installed and configured to use the lib.

## Installing AMI2RabbitMQ and Supported Versions

AMI2RabbitMQ is available on PyPI:

`$ python -m pip install ami2rabbitmq`

AMI2RabbitMQ officially supports Python 3.8+.

## Cloning the repository

`https://github.com/tatianno/ami2rabbitmq.git`

## Examples

### Simple producer application

```
from ami2rabbitmq import AMI2RabbitMQ


AMI_SETTINGS = {
    'host' : 'localhost',
    'user' : 'user',
    'password' : 'password'
}

RABBITMQ_SETTINGS = RABBITMQ_SETTINGS = {
    'host' : 'localhost',
    'user' : 'user',
    'password' : 'password',
    'queuename' : 'online'
}

producer = AMI2RabbitMQ(
    ami_settings = AMI_SETTINGS,
    rabbitmq_settings = RABBITMQ_SETTINGS,
)

producer.run()
```

### Advanced producer application

```
from ami2rabbitmq import AMI2RabbitMQ


AMI_SETTINGS = {
    'host' : 'localhost',
    'user' : 'user',
    'password' : 'password'
}

RABBITMQ_SETTINGS = RABBITMQ_SETTINGS = {
    'host' : 'localhost',
    'user' : 'user',
    'password' : 'password',
    'queuename' : 'online'
}


class CustomProducerApp(AMI2RabbitMQ):

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


custom_producer = CustomProducerApp(
    ami_settings = AMI_SETTINGS,
    rabbitmq_settings = RABBITMQ_SETTINGS,
)

custom_producer.run()
```