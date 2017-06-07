'''
Created on Oct 19, 2015

@author: cptullio
'''
from featuring.FeatureBase import FeatureBase
import networkx

class SPLFeature(FeatureBase):
    '''
    Shortest Path Length
    Nao possuindo path resultado  retornado = a quantidade de arestas existentes no grafo
    '''
    def __repr__(self):
        return 'SPL'
    
    def getName(self):
        return 'SPL'

    def __init__(self):
        super(SPLFeature, self).__init__()
        self.debugar = False
        
    
    
    def execute(self, node1, node2):
        if networkx.has_path(self.graph, node1, node2):
            final = self.getShortestPath(node1, node2)
            return len(final)
        else:
            return self.parameter.getQtyofEdges(self.graph)
        