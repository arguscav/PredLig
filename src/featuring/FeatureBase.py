'''
Created on Jun 16, 2015

@author: cptullio
'''
from abc import abstractmethod
import networkx as networkx

class FeatureBase(object):
    '''
    Base class for help prepare the features will be used
    '''
    def __init__(self):
        self.graph = None
        self.neighbors_node1 = None
        self.myneighbors = {}
        self.neighbors_node2 = None
        self.parameter = None
        self.debugar = False
    
    
    def getAllShortestPath(self, node1, node2):
        
        AllPaths = networkx.all_shortest_paths(self.graph, node1,  node2)
        AllCeanPath = []
        for path in AllPaths:
            lengthofPath = len(path)
            final = set()
            for index in range(lengthofPath-1):
                final.add( (path[index] , path[index+1]))
            if final not in AllCeanPath:    
                AllCeanPath.append(final)
        return AllCeanPath             
  
    
    def getShortestPath(self, node1, node2):
        SPpath = networkx.shortest_path(self.graph, node1,  node2)
        lengthofPath = len(SPpath)
        final =[]
        for index in range(lengthofPath-1):
            final.append([SPpath[index] , SPpath[index+1] ] )
        return final 
      
    
    
    
    def get_jacard_domain(self, bagofWordsNode1, bagofWordsNode2):
        f = (float)(len(bagofWordsNode1.intersection(bagofWordsNode2)))
        x = (float)(len(bagofWordsNode1.union(bagofWordsNode2)))
        if x == 0:
            return 0
        return f/x
    
    
    
    '''
    Get all informations of all neighbors of a node. 
    '''
    
    def get_ObjectsofNode(self, graph, mynode):
        return list(edge for n1,n2, edge in  graph.edges([mynode], data=True) if n1 == mynode or n2 == mynode )
    
    
    def get_ObjectsofLinks(self, graph, node1, node2):
        T3 = list(edge for n1, n2, edge in graph.edges([node1, node2], data=True) if ((n1 == node1 and n2 == node2) or (n1 == node2 and n2 == node1)) )
        return  T3
       
        
        
    
    
    
    def get_ObjectsofLinksWithMin_Edges(self, graph, node1, node2, min_edges):
        result = []
        edges = self.get_ObjectsofLinks(graph, node1, node2)
        for edge in edges:
            MaxAmplitude = self.parameter.t0_ - min_edges
            if edge['time'] >= MaxAmplitude:
                result.append(edge)
                
        return result

    
    #def generate_all_node_neighborsfromNode(self, node1):
    #    if node1 in self.myneighbors:
    #        return self.myneighbors[node1]
    #    self.myneighbors[node1] = set(self.all_node_neighbors(node1))
    #    return self.myneighbors[node1]
   
       
    @abstractmethod
    def execute(self, node1, node2):
        raise RuntimeError('not implemented')
    
    @abstractmethod
    def getName(self):
        raise RuntimeError('not implemented')
    
    def all_neighbors(self, node):
        return set(networkx.all_neighbors(self.graph, node))
    
    #from graph where the edge is define by other type of node
    #def all_node_neighbors(self, node):
    #    neighbors = set()
    #    for node_edge in list(networkx.all_neighbors(self.graph, node)):
    #        for neighbor in list(networkx.all_neighbors(self.graph, node_edge)):
    #            neighbors.add(neighbor)
    #    return neighbors - set([node])
    
    
    def get_common_neighbors(self, node1, node2):
        neighbors_node_1 = self.all_neighbors(node1)
        neighbors_node_2 = self.all_neighbors(node2)
        return neighbors_node_1.intersection(neighbors_node_2)    
    
        
    
