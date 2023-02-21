import json
from rabi import Rabi    
import threading
from pprint import pprint
import config
from controller import Controller
from fastapi import FastAPI,Form
import uvicorn
from pydantic import BaseModel
# from state_manager import StateManager

''' this is the main thread '''
# C = Controller(filepaths=["funcs"])
C = Controller()

def ack(ch, method, properties, body): 
    ''' shoud not know anything about dag obj '''

    print("---------- ack recieved ---------")
    print(" [x] Received %r" % body)
    res = json.loads(body)
    print(res["status"])
    print(C.dag_store)

    if res["dag_id"] not in C.dag_store.keys():
        print("DAG id not found in store")
        # print("pulling dag id, ",res["dag_id"])
        # fi = M.pull(res["dag_id"])
        # print("pulling file name, ",fi)
        # C.make([fi])
        # print(C.dag_store)
        return
    d = C.dag_store[res["dag_id"]]
    d.state[res["task_id"]] = res["status"]
    pprint(d.state)
    if res["status"]=='Success':
        print(d.g.vs.select(task_id_eq=res["task_id"]))
        C.push_next_tasks(d,d.g.vs.select(task_id_eq=res["task_id"])[0])

    elif res["status"]=='Failed':
        C.mark_next_tasks(dag_id = res["dag_id"],v = d.g.vs.select(task_id_eq=res["task_id"])[0],state = "Skipped")

def call_ctrl(ch, method, properties, body): 
    ''' shoud not know anything about dag obj '''

    print("---------- ctrl req recieved ---------")
    print(" [x] Received %r" % body)
    res = json.loads(body)
    print(res)
    C = Controller([res["dag"]])
    C.bake()
    print(C.dag_store)


def callback_func():
    r = Rabi(q = config.ACK_Q)
    r.listen_and_call(call= ack)
    r.close()

def callback_func_push():
    r = Rabi(q = config.CALL_Q)
    r.listen_and_call(call= call_ctrl)
    r.close()

# Start listening for ACK on another thread
listen_thread = threading.Thread(target=callback_func)
listen_thread.start()

# Start listening for ACK on another thread
listen_thread_2 = threading.Thread(target=callback_func_push)
listen_thread_2.start()
# callback_func_push()
