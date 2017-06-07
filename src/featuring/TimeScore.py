'''
Created on Jun 16, 2015

@author: cptullio
'''
from featuring.FeatureBase import FeatureBase
import networkx
from datetime import datetime

class TimeScore(FeatureBase):
    '''
    Original TimeScore Defined by Munasigne
    '''
    def __repr__(self):
        return 'ts'
    
    def getName(self):
        return 'ts'

    def __init__(self):
        super(TimeScore, self).__init__()
        self.times = {}
        self.debugar = False
        
    

    
    def execute(self, node1, node2):
        
        
        
        pair_common_neighbors  = self.get_common_neighbors(node1, node2)
        if len(pair_common_neighbors) == 0:
            return 0
        
        #print node1, node2, pair_common_neighbors
        timescoreValue = float(0)
        for pair_common_neighbor in pair_common_neighbors:
            timesofLinks = []
            timesofLinksNode1 = list (d['time'] for d in self.get_ObjectsofLinks(self.graph, node1, pair_common_neighbor))
            timesofLinksNode2 = list (d['time'] for d in self.get_ObjectsofLinks(self.graph, node2, pair_common_neighbor))
            
            timesofLinks.append(timesofLinksNode1)
            timesofLinks.append(timesofLinksNode2)
            
            #Harmonic Mean of Publications
            total = float(0)
            for publications in timesofLinks:
                total = total + 1/float(len(publications))
            hm = 2 / total
            #if self.debugar:
            #    print 'Harmonic meam:', hm
            print "IMPRIMINDO O MAXIMO DO TIMEOFLINKS PARA ENTENDER", max(list(timesofLinks))    
            k =  int(self.parameter.t0_)  - int(max(list(timesofLinks))[0])
            print "IMPRIMINDO O K", k    
            
            decayfunction = (1 - self.parameter.decay) ** k
            control = (abs( max(timesofLinksNode1) - max(timesofLinksNode2) ) + 1)
            ts = (hm * decayfunction) /control
            
            timescoreValue = timescoreValue + ts  
          
        return timescoreValue    
            
        