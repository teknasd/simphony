#!/usr/bin/env python
import pika, sys, os
from rabi import Rabi

def callback(ch, method, properties, body):
    print(ch, method, properties, body)
    print(" [x] Received %r" % body)

def main():
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # channel = connection.channel()

    # channel.queue_declare(queue='ex')
    # channel.basic_consume(queue='ex', on_message_callback=callback, auto_ack=True)

    # print(' [*] Waiting for messages. To exit press CTRL+C')
    # channel.start_consuming()

    r = Rabi(q = "ex")
    r.listen_and_call(call= callback)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)