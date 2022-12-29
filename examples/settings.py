DEBUG = True

AMI_SETTINGS = {
    'host' : '192.168.10.36',
    'user' : 'GNEW',
    'password' : 'MMtlcmm',
    'events' : [
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
}

RABBITMQ_SETTINGS = {
    'host' : '172.17.0.2',
    'user' : 'user',
    'password' : 'password',
    'queuename' : 'online'
}