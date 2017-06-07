'''
Created on Jun 16, 2015

@author: cptullio
'''
from featuring.FeatureBase import FeatureBase
import networkx
from datetime import datetime
import ast

class WeightDomainScore(FeatureBase):
    '''
    Domain Score Weighted by Carlos and Ronaldo
    '''
    def __repr__(self):
        return 'WDS'
    

    def __init__(self):
        super(WeightDomainScore, self).__init__()
        self.debugar = False
        
    
    
    
    def execute(self, node1, node2):
        
        
        
        informationsNode1 = self.get_ObjectsofNode(self.graph, node1)
        informationsNode2 = self.get_ObjectsofNode(self.graph, node2)
        
        bagofWordsNode1 = set()
        bagofWordsNode2 = set()
            
        for t1 in informationsNode1:
            for bt1 in t1[1]:
                bagofWordsNode1.add(bt1)
            for t2 in informationsNode2:
                for bt2 in t2[1]:
                    bagofWordsNode2.add(bt2)
                    
        jcKeyworkds = self.get_jacard_keywords(bagofWordsNode1, bagofWordsNode2)
        
        return jcKeyworkds    
            
        