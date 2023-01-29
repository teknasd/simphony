import igraph
import json
from pprint import pprint

'''
https://igraph.org/python/tutorial/0.9.7/tutorial.html#setting-and-retrieving-attributes
'''

class DAG():

    def __init__(self,user,data) -> None:
        self.dict_x = {}
        self.user = user
        try:
            self.data = json.load(open(data,"r"))
        except Exception:
            self.data = data
        # print(self.data)
        self._creation_status = True
        self.root = self.data["root"]
        self.list_of_nodes = self.data["nodes"]
        self.list_of_links = self.data["links"]
        pprint(self.data)

    def create_graph(self):
        self.g = igraph.Graph(directed =True)
        self._fill_nodes()
        self._fill_connections()

        #g.add_vertices(self.list_of_nodes)
    def _print_allnodes(self):
        for n in self.g.vs:
            pass
        
    def _fill_nodes(self):
        for e,node in enumerate(self.data["nodes"]):
            self.g.add_vertex(node)
            # self.g.vs[e]["nodeId"] = node
            # self.g.vs[e]["type"] = self.data["nodes"][node]["type"]

            # self.g.vs[e]["ports"] = self.data["nodes"][node]["ports"]
            # self.g.vs[e]["conditions"] = self.data["nodes"][node]["conditions"]

    def _get_vertex_id(self,id_):
        p = self.g.vs.find(name = id_)
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


    
    def debugMessage(funName, *args):
        try:
            print("--------------------")
            pprint(funName, "-", args)
        except:
            pass

    def getListOfObjects(self,data,type):
        listOfObject = []
        for key in data['nodes'].keys():
            if(data['nodes'][key]['type'] == type):
                tmpData = {key:data['nodes'][key]['properties']['name']}
                listOfObject.append(tmpData)
        return listOfObject


    def nodes_list(self,data):
        keylist = data.keys()
        self.debugMessage("nodes_list", "Key list:-", keylist)

    def get_link_info(self,data):
        for key in data['links'].keys():
            self.debugMessage("get_link_info", key)


    def get_neighbors(self,vertex = None):
        vertex = self.g.vs.find(name= self.root) if vertex is None else vertex
        return self.g.neighborhood(vertices=vertex, order=1, mode='out',mindist = 1)

    # def 


    