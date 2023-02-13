import igraph
import importlib
import json
from pprint import pprint
from uuid import uuid4
from rshift import Make

'''
https://igraph.org/python/tutorial/0.9.7/tutorial.html#setting-and-retrieving-attributes
'''

class DAG():

    def __init__(self,user,filepath=None) -> None:
        self.dict_x = {}
        self.user = user
        self.dag_id = str(uuid4())
        self.state = dict()
        self.filepath = str(filepath)
        self.dag = self.filepath.split(".")[0].replace('/','.')
        # print(self.dag)
        try:
            self.data = json.load(open(filepath,"r"))
        except Exception:
            self.data = None
        # print(self.data)

        if self.data is not None:
            self._creation_status = True
            self.root = self.data["root"]
            self.list_of_nodes = self.data["nodes"]
            self.list_of_links = self.data["links"]
        # pprint(self.data)
    
    # def __repr__(self):
    #     return f"DAG id: {self.dag_id}"
    
    def create_graph_py(self):
        module = importlib.import_module(self.dag)
        self.module_vars = vars(module)
        print(Make.flow)
        self.flow = self.module_vars['Make'].flow
        self.nodes = self.module_vars['Make'].nodes #self._find_nodes()
        self.nodes_count = len(self.nodes)
        self.g = igraph.Graph(self.nodes_count,directed =True)
        self._fill_nodes()
        self._fill_connections()
        Make.flow = []
        Make.nodes = set()
        

    def _find_nodes(self):
        return set(t.func.__name__ for f in self.flow for t in f )
    def _count_nodes(self):
        return len(self.nodes)

    def create_graph(self): 
        nodes = len(self.data["nodes"])
        self.g = igraph.Graph(nodes,directed =True)
        self._fill_nodes()
        self._fill_connections()

    def _fill_nodes(self):
        for e,task in enumerate(self.nodes):
            self.g.vs[e]["task"] = task #task.func.__name__
            self.g.vs[e]["task_id"] = str(uuid4())
            self.state[self.g.vs[e]["task_id"]] = "Pending"


    def _get_vertex_id(self,id_):
        # print(id_)
        p = self.g.vs.find(task = id_)
        # print(p.index)
        return p.index

    def _fill_connections(self):
        list_of_edges = [
            (
                self._get_vertex_id(edge[0].func.__name__),
                self._get_vertex_id(edge[1].func.__name__),
            )
            for edge in self.flow
        ]
        self.g.add_edges(list_of_edges)

    # def _fill_connections(self):
    #     list_of_edges = [
    #         (
    #             self._get_vertex_id(self.data["links"][edge][0]),
    #             self._get_vertex_id(self.data["links"][edge][1]),
    #         )
    #         for edge in self.data["links"].keys()
    #     ]
    #     self.g.add_edges(list_of_edges)

    def find_root_nodes(self):
        # find the root node(s)
        return [v.index for v in self.g.vs if v.indegree() == 0]

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
