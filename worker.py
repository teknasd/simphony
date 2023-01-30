#!/usr/bin/env python
import sys, os
from rabi import Rabi
from pprint import pprint
import json
import funcs
import traceback

def callback(ch, method, properties, body):
    print("---------- recieved ---------")
    pprint(ch.__dict__)
    print(" [x] Received %r" % body)
    params = json.loads(body)
    print(params)
    print("---------- start ------------")

    try:
        module = __import__(params['dag'])
        func = getattr(module, params['call'])
        func()
        emit_ack(params['call'])
        
    except Exception:
        print(f'There is some error at {traceback.format_exc()}')
    print("---------- end ------------")

def emit_ack(call):
    r = Rabi(q = "ack")
    r.push_to_q(json.dumps({"status":"success","call":call}))

def main():
    r = Rabi(q = "ex")
    r.listen_and_call(call= callback)
    print("********************")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)