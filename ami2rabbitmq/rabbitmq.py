import json
import pika


class RabbitMQProducer():
    __connection = None
    __channel = None
    

    def __init__(self, rabbitmq_settings, logs_app):
        self.host = rabbitmq_settings['host']
        self.username = rabbitmq_settings['user']
        self.password = rabbitmq_settings['password']
        self.queuename = rabbitmq_settings['queuename']
        self._logs_app = logs_app

    def connect(self):
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                credentials=pika.PlainCredentials(
                    self.username, 
                    self.password    
                )
            )
        )
        self.__channel = self.__connection.channel()
        self.__channel.queue_declare(queue=self.queuename)

    def disconnect(self):
        self.__connection.close()
    
    def __rabbitmq_send__(self, mensagem):
        self.__channel.basic_publish(
            exchange='',
            routing_key=self.queuename,
            body=mensagem
        )
                       
    def send(self, mensagem):
        try:
            self.connect()
            self.__rabbitmq_send__(
                json.dumps(mensagem)
            )
            self.disconnect()
        
        except pika.exceptions.AMQPConnectionError as error:
            self._logs_app.register('Fail connection RabbitMQ')