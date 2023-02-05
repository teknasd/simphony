import json
from dag import DAG
from rabi import Rabi    
import threading
from pprint import pprint

d = DAG(user = 1, data = "./dag.json")
d.create_graph()

def init():
    # r = Rabi(q = "ex")
    print(f"----------> {d.root }")
    vertex_id = d.g.vs.find(task = d.root)
    push_task_to_q(vertex_id.index)


def push_task_to_q(t):
    task_obj = json.dumps(
                {
                    "dag":"funcs",
                    "call":d.g.vs[t]['task'],
                    "task_id":d.g.vs[t]['task_id'],
                    "dag_id":d.dag_id,
                    }
                )
    r = Rabi(q = "ex")
    r.push_to_q(task_obj)

def push_next_tasks(v):
    tasks = d.get_neighbors(vertex=v)
    print("tasks",tasks)
    
    for t in tasks:
        print("t:",t)
        print("v:",d.g.vs[t]['task'])
        d.state[d.g.vs[t]["task_id"]] = "Queued"
        push_task_to_q(t)

def mark_next_tasks(v,state):
    tasks = d.get_neighbors(vertex=v)
    print("tasks",tasks)
    for t in tasks:
        print("t:",t)
        print("v:",d.g.vs[t]['task'])
        d.state[d.g.vs[t]["task_id"]] = state
        mark_next_tasks(t,state="Skipped")
    
def ack(ch, method, properties, body): 
    ''' shoud not know anything about dag obj '''

    print("---------- ack recieved ---------")
    print(" [x] Received %r" % body)
    res = json.loads(body)
    print(res["status"])
    d.state[res["task_id"]] = res["status"]
    pprint(d.state)
    if res["status"]=='Success':
        print(d.g.vs.select(task_id_eq=res["task_id"]))
        push_next_tasks(d.g.vs.select(task_id_eq=res["task_id"])[0])

    elif res["status"]=='Failed':
        mark_next_tasks(v = d.g.vs.select(task_id_eq=res["task_id"])[0],state = "Skipped")


def callback_func():
    r = Rabi(q = "ack")
    r.listen_and_call(call= ack)

init()


# # Start sending message on one thread
# send_thread = threading.Thread(target=send_message)
# send_thread.start()


# Start listening for ACK on another thread
listen_thread = threading.Thread(target=callback_func)
listen_thread.start()


