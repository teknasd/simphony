import json
from dag import DAG
from rabi import Rabi    
import threading
from pprint import pprint

# dag_store = {}
filepath = "dags.funcs"

class Controller:

    def __init__(self,filepaths=None):
        # for all dag in dags folder
        
        self.dag_store = {}
        if filepaths is None:
            files = self._read_dags_path()
        else:
            files = filepaths
        print(files)
        for fi in files:
            d = DAG(user = 1, filepath = fi)
            d.create_graph_py()
            self.dag_store[d.dag_id] = d
            print(self.dag_store)
            for node in d.find_root_nodes():
                self.push_task_to_q(d,node)

    def _read_dags_path(self):
        from glob import glob
        return glob("dags/*.py",recursive = False)


    def push_task_to_q(self,d,t):
        task_obj = json.dumps(
                    {
                        "dag":d.dag,
                        "call":d.get_v_val(t,'task'),
                        "task_id":d.get_v_val(t,'task_id'),
                        "dag_id":d.dag_id,
                        }
                    )
        r = Rabi(q = "ex")
        r.push_to_q(task_obj)
        r.close()


    def push_next_tasks(self,d,v):
        tasks = d.get_neighbors(vertex=v)
        print("tasks",tasks)
        
        for t in tasks:
            print("t:",t)
            # print("v:",self.d.get_v_val(t,'task'))
            d.state[d.get_v_val(t,'task_id')] = "Queued"
            self.push_task_to_q(d,t)

    def mark_next_tasks(self,dag_id,v,state):
        ''' mark all the succedding task with the given state by using bfs'''
        d = self.dag_store[dag_id]
        tasks = d.get_neighbors(vertex=v)
        for t in tasks:
            d.state[d.get_v_val(t,'task_id')] = state
            self.mark_next_tasks(dag_id,t,state=state)
        
def ack(ch, method, properties, body): 
    ''' shoud not know anything about dag obj '''

    print("---------- ack recieved ---------")
    print(" [x] Received %r" % body)
    res = json.loads(body)
    print(res["status"])

    print(C.dag_store)

    if res["dag_id"] not in C.dag_store.keys():
        print("DAG id not found in store")
        return
    d = C.dag_store[res["dag_id"]]
    d.state[res["task_id"]] = res["status"]
    pprint(d.state)
    if res["status"]=='Success':
        print(d.g.vs.select(task_id_eq=res["task_id"]))
        C.push_next_tasks(d,d.g.vs.select(task_id_eq=res["task_id"])[0])

    elif res["status"]=='Failed':
        C.mark_next_tasks(dag_id = res["dag_id"],v = d.g.vs.select(task_id_eq=res["task_id"])[0],state = "Skipped")


def callback_func():
    r = Rabi(q = "ack")
    r.listen_and_call(call= ack)
    r.close()


# C = Controller(filepaths=["funcs"])
C = Controller()

# # Start sending message on one thread
# send_thread = threading.Thread(target=send_message)
# send_thread.start()


# Start listening for ACK on another thread
listen_thread = threading.Thread(target=callback_func)
listen_thread.start()


