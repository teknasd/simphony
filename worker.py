#!/usr/bin/env python
import sys, os
from rabi import Rabi
from pprint import pprint
import json
import traceback
from retry import retry
import time
import importlib
from state_manager import StateManager
import config as config
import threading

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
@retry(tries = config.TASK_RETRY_COUNT)
def runtime_func(params):
    module = importlib.import_module(params['dag'])
    func = getattr(module, params['call'])
    M = StateManager(manager = config.STATE_MANAGER)
    curr_state = M.pull(params["dag"])
    print("curr_state:",curr_state)
    ''' actual function call passed by dag '''
    curr_state = func(curr_state)
    M.push(params["dag"],curr_state)
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
    r = Rabi(q = config.ACK_Q)
    p["status"] = status
    pprint(p)
    r.push_to_q(json.dumps(p))
    r.close()

class ConcurrencyManager():
    def __init__(self,concurr = 1):
        ConcurrencyManager.concurr = concurr
        ConcurrencyManager.thread_mgr = {}

    def bootup(self,func_call):
        # start new thread for CONCURRENCY in config
        for i in range(ConcurrencyManager.concurr + 1):
            listen_thread = threading.Thread(target=func_call)
            listen_thread.start()
            ConcurrencyManager.thread_mgr[i] = listen_thread
    def stop_threads(self):
        for th in len(ConcurrencyManager.thread_mgr):
            th.join()

def brocker_listner():
    r = Rabi(q = config.EX_Q)
    r.listen_and_call(call= callback)
    print("********************")
    r.close()

def main():
    ConcurrencyManager(concurr = config.CONCURRENCY).bootup(brocker_listner)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Main exucution thread interrupted | Now closing all the worker threads')
        ConcurrencyManager.stop_threads()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)