#!/usr/bin/env python
import pika
from config import RABBIT_CON

class Rabi():
    def __init__(self,q = None):
        ConnectionParameters = pika.ConnectionParameters(RABBIT_CON["LOCATION"],RABBIT_CON["PORT"])
        self.connection = pika.BlockingConnection(ConnectionParameters)
        self.channel = self.connection.channel()
        self.connect()
        self.q = "default" if q is None else q
        self._queue_declare(q=self.q)
        self.channel.basic_qos(prefetch_count=1)

    def connect(self):
        ConnectionParameters = pika.ConnectionParameters(RABBIT_CON["LOCATION"],RABBIT_CON["PORT"])
        self.connection = pika.BlockingConnection(ConnectionParameters)
        self.channel = self.connection.channel()
    
    def check_and_reconnect(self):
        if self.connection.is_closed:
            self.connect()

    def _queue_declare(self,q):
        self.channel.queue_declare(queue=q, durable=True)

    def push_to_q(self,context=""):
        # context is str
        res = self.channel.basic_publish(exchange='',
                            routing_key=self.q,
                            body=context)
        print(f"***** push to q : {context}")

    def listen_and_call(self,q=None,call=None):
        ''' Continously listen on seperate thread '''
        if q is None:
            q = self.q
        self.channel.basic_consume(queue=q, on_message_callback=call, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
