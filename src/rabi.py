#!/usr/bin/env python
import pika
from config import RABBIT_CON
from log_manager import logger

class Rabi():
    def __init__(self,q = None,async_ = False):

        if async_ == False:
            self.connect()
            self.q = "default" if q is None else q
            self._queue_declare(q=self.q)
            self.channel.basic_qos(prefetch_count=1)
        else:
            # self.connect_async()
            pass


    def connect(self):
        ConnectionParameters = pika.ConnectionParameters(RABBIT_CON["LOCATION"],RABBIT_CON["PORT"])
        self.connection = pika.BlockingConnection(ConnectionParameters)
        self.channel = self.connection.channel()
    def connect_async(self,on_open):
        ConnectionParameters = pika.ConnectionParameters(RABBIT_CON["LOCATION"],RABBIT_CON["PORT"])
        self.connection = pika.SelectConnection(ConnectionParameters,on_open_callback=on_open)
        # self.channel = self.connection.channel()


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
        logger.info(f"***** push to q : {context}")

    def listen_and_call(self,q=None,call=None):
        ''' Continously listen on seperate thread '''
        if q is None:
            q = self.q
        self.channel.basic_consume(queue=q, on_message_callback=call, auto_ack=True)

        logger.info(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
