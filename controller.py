import json
from dag import DAG
from rabi import Rabi    
import threading
from pprint import pprint

# dag_store = {}
filepath = "./dag.json"

class Controller:

    def __init__(self,filepath):
        self.d = DAG(user = 1, data = filepath)
        self.d.create_graph()
        # self.dag_store[d.dag_id] = d
        self.dag_store = {
            self.d.dag_id : self.d
        }
        print(f"----------> {self.d.root }")
        vertex_id = self.d.g.vs.find(task = self.d.root)
        self.push_task_to_q(vertex_id.index)


    def push_task_to_q(self,t):
        task_obj = json.dumps(
                    {
                        "dag":"funcs",
                        "call":self.d.get_v_val(t,'task'),
                        "task_id":self.d.get_v_val(t,'task_id'),
                        "dag_id":self.d.dag_id,
                        }
                    )
        r = Rabi(q = "ex")
        r.push_to_q(task_obj)

    def push_next_tasks(self,v):
        tasks = self.d.get_neighbors(vertex=v)
        print("tasks",tasks)
        
        for t in tasks:
            print("t:",t)
            print("v:",self.d.get_v_val(t,'task'))
            self.d.state[self.d.get_v_val(t,'task_id')] = "Queued"
            self.push_task_to_q(t)

    def mark_next_tasks(self,v,state):
        ''' mark all the succedding task with the given state by using bfs'''
        tasks = self.d.get_neighbors(vertex=v)
        for t in tasks:
            self.d.state[self.d.get_v_val(t,'task_id')] = state
            self.mark_next_tasks(t,state="Skipped")
        
def ack(ch, method, properties, body): 
    ''' shoud not know anything about dag obj '''

    print("---------- ack recieved ---------")
    print(" [x] Received %r" % body)
    res = json.loads(body)
    print(res["status"])
    d = C.dag_store[res["dag_id"]]
    d.state[res["task_id"]] = res["status"]
    pprint(d.state)
    if res["status"]=='Success':
        print(d.g.vs.select(task_id_eq=res["task_id"]))
        C.push_next_tasks(d.g.vs.select(task_id_eq=res["task_id"])[0])

    elif res["status"]=='Failed':
        C.mark_next_tasks(v = d.g.vs.select(task_id_eq=res["task_id"])[0],state = "Skipped")


def callback_func():
    r = Rabi(q = "ack")
    r.listen_and_call(call= ack)


C = Controller(filepath=filepath)


# # Start sending message on one thread
# send_thread = threading.Thread(target=send_message)
# send_thread.start()


# Start listening for ACK on another thread
listen_thread = threading.Thread(target=callback_func)
listen_thread.start()


