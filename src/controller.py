import json, os
from dag import DAG
from rabi import Rabi    
import threading
from pprint import pprint
from state_manager import StateManager
import config
from log_manager import logger


class Controller:

    def __init__(self,filepaths=None):
        # for all dag in dags folder
        
        Controller.dag_store = {}
        if filepaths is None:
            self.files = self._read_dags_path()
        else:
            self.files = filepaths
        logger.info(self.files)
        # self.bake()
        
    def bake(self,contexts):
        logger.info("inside baking")
        for fi,con in zip(self.files,contexts):
            # check if file exists
            # if os.path.exists(fi):
            d = DAG(user = 1, filepath = fi)
            d.create_graph_py()
            Controller.dag_store[d.dag_id] = d
            logger.info(Controller.dag_store)
            self._save(d.dag_id,con)
            for node in d.find_root_nodes():
                self.push_task_to_q(d,node)
            # else:
            #     print(f"{fi} does not exist.")

    def make(self,files):
        for fi in files:
            d = DAG(user = 1, filepath = fi)
            d.create_graph_py()
            Controller.dag_store[d.dag_id] = d

    def _save(self,key,val):
        M = StateManager(manager = config.STATE_MANAGER)
        M.push(key,val)

    def _read_dags_path(self):
        from glob import glob
        return glob(f"{config.DAG_FOLDER}/*.py",recursive = False)


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
        logger.info("tasks",tasks)
        
        for t in tasks:
            logger.info("t:",t)
            # print("v:",self.d.get_v_val(t,'task'))
            d.state[d.get_v_val(t,'task_id')] = "Queued"
            self.push_task_to_q(d,t)

    def mark_next_tasks(self,dag_id,v,state):
        ''' mark all the succedding task with the given state by using bfs'''
        d = Controller.dag_store[dag_id]
        tasks = d.get_neighbors(vertex=v)
        for t in tasks:
            d.state[d.get_v_val(t,'task_id')] = state
            self.mark_next_tasks(dag_id,t,state=state)
