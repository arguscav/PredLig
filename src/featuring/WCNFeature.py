'''
Created on Oct 4, 2015

@author: cptullio
'''
from featuring.FeatureBase import FeatureBase

class WCNFeature(FeatureBase):
    '''
    Weighted Common Neighbor by Linyuan Lu and Tao
    '''
    def __repr__(self):
        return 'WCN'
    
    def getName(self):
        return 'WCN'

    def __init__(self):
        super(WCNFeature, self).__init__()
        self.debugar = False
        
    
    
    
    def execute(self, node1, node2, weight_index):
        print 'indice a ser usado: ', weight_index
        cnList = self.get_common_neighbors(node1, node2)
        total = 0
        
        for cn in cnList:
            total = total + ( float(self.parameter.get_weights(node1, cn)[int(weight_index)])  + float(self.parameter.get_weights(node2, cn )[int(weight_index)]))
            
        return total
            
        