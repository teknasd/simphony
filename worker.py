#!/usr/bin/env python
import sys, os
from rabi import Rabi
from pprint import pprint
import json
import traceback
from retry import retry

def pre_post_signal(func):
    def wrapper(*args, **kwargs):
        params = kwargs["params"]
        try:
            result = func(*args, **kwargs)
            emit_ack(params,"Success")
            return result
        except Exception:
            emit_ack(params,"Failed")
            print(f'There is some error at {traceback.format_exc()}')
            return False

    return wrapper

@pre_post_signal
@retry(tries = 3)
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

def emit_ack(p,status):
    r = Rabi(q = "ack")
    r.push_to_q(json.dumps({"status":status,"call":p["call"],"task_id":p["task_id"]}))

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