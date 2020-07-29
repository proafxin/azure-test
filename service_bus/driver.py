from message_queue import ServiceBus

if __name__ == "__main__":
    bus = ServiceBus()
    sender = bus.get_sender(queue_name='testsender')
    receiver = bus.get_receiver(queue_name='testreceiver')
