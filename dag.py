import igraph
import json
from pprint import pprint
from uuid import uuid4

'''
https://igraph.org/python/tutorial/0.9.7/tutorial.html#setting-and-retrieving-attributes
'''

class DAG():

    def __init__(self,user,data) -> None:
        self.dict_x = {}
        self.user = user
        self.dag_id = str(uuid4())
        try:
            self.data = json.load(open(data,"r"))
        except Exception:
            self.data = data
        # print(self.data)
        self._creation_status = True
        self.root = self.data["root"]
        self.list_of_nodes = self.data["nodes"]
        self.list_of_links = self.data["links"]
        self.state = dict()
        pprint(self.data)

    def create_graph(self):
        nodes = len(self.data["nodes"])
        self.g = igraph.Graph(nodes,directed =True)
        self._fill_nodes()
        self._fill_connections()

        
    def _fill_nodes(self):
        for e,task in enumerate(self.data["nodes"]):
            # n = {"node":node,"task_id":uuid4()}
            self.g.vs[e]["task"] = task
            self.g.vs[e]["task_id"] = str(uuid4())
            self.state[self.g.vs[e]["task_id"]] = "Pending"


    def _get_vertex_id(self,id_):
        p = self.g.vs.find(task = id_)
        print(p.index)
        return p.index

    def _fill_connections(self):
        list_of_edges = [
            (
                self._get_vertex_id(self.data["links"][edge][0]),
                self._get_vertex_id(self.data["links"][edge][1]),
            )
            for edge in self.data["links"].keys()
        ]
        self.g.add_edges(list_of_edges)

    def get_v_val(self,id,key):
        return self.g.vs[id][key]

    def nodes_list(self,data):
        keylist = data.keys()
        self.debugMessage("nodes_list", "Key list:-", keylist)

    def get_link_info(self,data):
        for key in data['links'].keys():
            self.debugMessage("get_link_info", key)


    def get_neighbors(self,vertex = None):
        vertex = self.g.vs.find(task= self.root) if vertex is None else vertex
        return self.g.neighborhood(vertices=vertex, order=1, mode='out',mindist = 1)
