import json
from dag import DAG
from rabi import Rabi    
import threading

d = DAG(user = 1, data = "./dag.json")
d.create_graph()

def init():
    r = Rabi(q = "ex")
    print(f"----------> {d.root }")
    root_task = d.root 
    r.push_to_q(json.dumps({"dag":"funcs","call":root_task}))



def push_next_tasks(v):
    tasks = d.get_neighbors(vertex=v)
    print("tasks",tasks)
    r = Rabi(q = "ex")
    for t in tasks:
        print("t:",t)
        print("v:",d.g.vs[t]['name'])
        r.push_to_q(json.dumps({"dag":"funcs","call":d.g.vs[t]['name']}))
    
def ack(ch, method, properties, body):
    print("---------- recieved ---------")
    print(ch.__dict__)
    print(" [x] Received %r" % body)
    res = json.loads(body)
    print(res["status"])
    print(d.g.vs.select(name_eq=res["call"]))
    push_next_tasks(d.g.vs.select(name_eq=res["call"])[0])



def load_next():

        
    r = Rabi(q = "ack")
    r.listen_and_call(call= ack)



# while 
init()


# # Start sending message on one thread
# send_thread = threading.Thread(target=send_message)
# send_thread.start()


# Start listening for ACK on another thread
listen_thread = threading.Thread(target=load_next)
listen_thread.start()


