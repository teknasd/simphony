#!/usr/bin/env python
import sys, os
from rabi import Rabi
from pprint import pprint
import json
import traceback

def pre_post_signal(func):
    def wrapper(*args, **kwargs):
        params = kwargs["params"]
        try:
            result = func(*args, **kwargs)
            emit_ack(params['call'],"success")
            return result
        except Exception:
            emit_ack(params['call'],"failed")
            print(f'There is some error at {traceback.format_exc()}')
            return False

    return wrapper

@pre_post_signal
def runtime_func(params):
    module = __import__(params['dag'])
    func = getattr(module, params['call'])
    func()
    return True
    
def callback(ch, method, properties, body):
    print("---------- recieved ---------")
    # pprint(ch.__dict__)
    print(" [x] Received %r" % body)
    params = json.loads(body)
    print(params)
    print("---------- start ------------")
    runtime_func(params=params)
    print("---------- end ------------")

def emit_ack(call,status):
    r = Rabi(q = "ack")
    r.push_to_q(json.dumps({"status":status,"call":call}))

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