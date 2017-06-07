'''
Created on Jun 16, 2015

@author: cptullio
'''
from featuring.FeatureBase import FeatureBase
import networkx
from datetime import datetime
import ast

class WeightTimeScore(FeatureBase):
    '''
    Time Score Weighted by Carlos and Ronaldo
    '''
    def __repr__(self):
        return 'WTS'
    

    def __init__(self):
        super(WeightTimeScore, self).__init__()
        self.debugar = False
        
    
    
    
    def execute(self, node1, node2):
        informations = self.get_ObjectsofLinks(self.graph, node1, node2)
        if len(informations) == 0:
            return 0
        
        timesofLinks = []
        for info in informations:
            timesofLinks.append(int(info['time']))
        
               
        total_publications = len(informations)   
        k =  int(self.parameter.t0_)  - max(timesofLinks)
        decayfunction = (1 - self.parameter.decay) ** k
            
        return total_publications * decayfunction    
            
        