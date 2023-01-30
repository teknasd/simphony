import json
from dag import DAG
from rabi import Rabi    
import threading

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
                    "job_id":d.job_id,
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
        push_task_to_q(t)

    
def ack(ch, method, properties, body): 
    print("---------- ack recieved ---------")
    # print(ch.__dict__)
    print(" [x] Received %r" % body)
    res = json.loads(body)
    print(res["status"])
    if res["status"]=='success':
        print(d.g.vs.select(task_eq=res["call"]))
        push_next_tasks(d.g.vs.select(task_eq=res["call"])[0])



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


