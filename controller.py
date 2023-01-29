import json
from dag import DAG
from rabi import Rabi    


d = DAG(user = 1, data = "./dag.json")
d.create_graph()

r = Rabi(q = "ex")
ack = Rabi(q = "ack")
print(f"----------> {d.root }")
root_task = d.root 
r.push_to_q(json.dumps({"call":root_task}))
# wait for ack
d.get_neighbors()

def push_all_tasks():
    tasks = d.get_neighbors()
    for t in tasks:
        r.push_to_q(t)

# while 
