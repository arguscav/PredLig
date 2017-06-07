'''
Created on Jun 16, 2015

@author: cptullio
'''
from featuring.FeatureBase import FeatureBase
import networkx
from datetime import datetime
import ast

class DomainJC(FeatureBase):
    '''
    Domain Jaccard by Carlos and Ronaldo
    '''
    def __repr__(self):
        return 'DJC'
    
    def getName(self):
        return 'DJC'    

    def __init__(self):
        super(DomainJC, self).__init__()
        self.debugar = False
        
       
        
    def execute(self, node1, node2):
        
        pair_common_neighbors  = self.get_common_neighbors(node1, node2)
        if len(pair_common_neighbors) == 0:
            return 0
        if self.debugar:
            print node1, node2, pair_common_neighbors
        
        domainJCValue = float(0)
        for pair_common_neighbor in pair_common_neighbors:
            objectsNode1 = self.get_ObjectsofLinks(self.graph, node1, pair_common_neighbor)
            objectsNode2 = self.get_ObjectsofLinks(self.graph, node2, pair_common_neighbor)
            
            bagofWordsNode1 = set()
            bagofWordsNode2 = set()
            
            for t1 in objectsNode1:
                for bt1 in t1['keywords']:
                    bagofWordsNode1.add(bt1)
            for t2 in objectsNode2:
                for bt2 in t2['keywords']:
                    bagofWordsNode2.add(bt2)
            
            
            jcKeyworkds = self.get_jacard_domain(bagofWordsNode1, bagofWordsNode2)
            if self.debugar:
                print 'bags node1 and node2:', bagofWordsNode1, bagofWordsNode2
                print 'Jc keyworkds: ', jcKeyworkds
            domainJCValue = domainJCValue + jcKeyworkds
            
        return domainJCValue    
            
        