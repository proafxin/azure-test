import logging

from os import getcwd
from os.path import join
from json import loads
from datetime import datetime
from azure.servicebus import ServiceBusClient


class ServiceBus:
    __pwd = getcwd()
    client_ = None

    def __init__(self):
        filename = 'service_bus_creds.json'
        creds_file = join(self.__pwd, filename)
        f = open(creds_file)
        creds = loads(f.read())
        #print(creds)
        keys = creds.keys()
        keys = list(keys)
        print(keys)
        conn_str = creds[keys[1]]
        try:
            client = ServiceBusClient.from_connection_string(conn_str)
            self.client_ = client
            print('Successfully connected to service bus: '+creds[keys[1]])
        except:
            raise ConnectionError('Failed to connect to service bus with connection string: '+creds[keys[1]])

    def get_sender(self, queue_name='testqueue'):
        bus = self.client_
        try:
            sender = bus.get_queue_sender(queue_name=queue_name)
            print('Successfully connected to sender: '+sender._entity_name)
        except:
            raise ConnectionRefusedError('Could not connect to sender: '+sender._entity_name)

    def get_receiver(self, queue_name='testqueue'):
        bus = self.client_
        try:
            receiver = bus.get_queue_receiver(queue_name=queue_name)
            print('Successfully connected to receiver: '+receiver._entity_name)
        except:
            raise ConnectionRefusedError('Could not connect to receiver: '+receiver._entity_name)