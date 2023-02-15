#!/usr/bin/env python
import sys, os
from rabi import Rabi
from pprint import pprint
import json
import traceback
from retry import retry
import time
import importlib
from state_manager import *

def pre_post_signal(func):
    def wrapper(*args, **kwargs):
        params = kwargs["params"]
        try:
            st_time = time.monotonic()
            result = func(*args, **kwargs)
            en_time = time.monotonic()
            print(f"time taken: {en_time- st_time} secs")
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
    module = importlib.import_module(params['dag'])
    func = getattr(module, params['call'])
    curr_state = pull(params["dag"])
    ''' actual function call passed by dag '''
    curr_state = func(curr_state)
    push(params["dag"],curr_state)
    return True
    
def callback(ch, method, properties, body):
    print("---------- recieved ---------")
    # pprint(ch.__dict__)
    print(" [x] Received %r" % body)
    params = json.loads(body)
    print(params)
    print("---------- start ------------")
    runtime_func(params=params)
    print("---------- end --------------\n\n\n")

def emit_ack(p,status):
    r = Rabi(q = "ack")
    p["status"] = status
    pprint(p)
    r.push_to_q(json.dumps(p))
    r.close()

def main():
    r = Rabi(q = "ex")
    r.listen_and_call(call= callback)
    print("********************")
    r.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)