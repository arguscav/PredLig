'''
Created on Oct 4, 2015

@author: cptullio
'''
from featuring.FeatureBase import FeatureBase


class PAWFeature(FeatureBase):
    '''
    Weighted Preferential Attachment by Muratta
    '''
    def __repr__(self):
        return 'PAW'
    
    def getName(self):
        return 'PAW'

    def __init__(self):
        super(PAWFeature, self).__init__()
        self.debugar = False
        
    
    
    
    def execute(self, node1, node2, weight_index):
        print 'indice a ser usado: ', weight_index
        
        Total_Node1 = 0
        for z in self.all_neighbors(node1):
            Total_Node1 = Total_Node1 + float(self.parameter.get_weights(z, node1)[int(weight_index)]) 
        Total_Node2 = 0
        for y in self.all_neighbors(node2):
            Total_Node2 = Total_Node2 + float(self.parameter.get_weights(y, node2)[int(weight_index)]) 
        
        
        return Total_Node1 * Total_Node2
        
            
        