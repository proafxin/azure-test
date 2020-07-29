import logging

from os.path import (
    join,
    dirname,
)
from json import loads
from datetime import datetime
from azure.servicebus import ServiceBusClient


class ServiceBus:
    """
    In order to make the path absolute, get the directory name of the current file.
    We are assuming that the credential file will be placed into the same directory.
    """
    __pwd = dirname(__file__)
    client_ = None

    def __init__(self):
        """
        For now we will keep the credential file hardcoded since there is one service bus here
        """
        filename = 'service_bus_creds.json'
        print(self.__pwd)
        """
        Read the credential file and load it into a json object.
        A lot of people do not follow this practice and keep the file names relative.
        Avoid relative path naming as much as possible.
        """
        creds_file = join(self.__pwd, filename)
        f = open(creds_file)
        creds = loads(f.read())
        #print(creds)
        keys = creds.keys()
        keys = list(keys)
        print(keys)
        """
        We used keys[1] to avoid writing a big key name.
        Make sure your json object has the same fields as the one in the template file.
        """
        conn_str = creds[keys[1]]
        """
        Add a try/except module for checking. We may dump the log in a file later if necessary
        """
        try:
            client = ServiceBusClient.from_connection_string(conn_str)
            self.client_ = client
            print('Successfully connected to service bus: '+creds[keys[1]])
        except:
            raise ConnectionError('Failed to connect to service bus with connection string: '+creds[keys[1]])

    def get_sender(self, queue_name='testqueue'):
        """
        Connect to the named queue of the service bus specified in the credential file.
        Use this method only to send to the said queue.

        Parameters:
            queue_name: string, default = testqueue
            the name of the queue you want to use as sender
        """
        bus = self.client_
        try:
            sender = bus.get_queue_sender(queue_name=queue_name)
            """
            Check that the connected queue is indeed the queue we passed on in the argument.
            The _entity_name attribute of the client contains the name of the queue
            """
            print('Successfully connected to sender: '+sender._entity_name)
        except:
            raise ConnectionRefusedError('Could not connect to sender: '+sender._entity_name)

    def get_receiver(self, queue_name='testqueue'):
        """
        This is same as the sender above. It will only be used for receiving messages

        Parameters:
            queue_name: string, default=testqueue
            the name of the queue you want to consume messages from
        """
        bus = self.client_
        try:
            receiver = bus.get_queue_receiver(queue_name=queue_name)
            print('Successfully connected to receiver: '+receiver._entity_name)
        except:
            raise ConnectionRefusedError('Could not connect to receiver: '+receiver._entity_name)