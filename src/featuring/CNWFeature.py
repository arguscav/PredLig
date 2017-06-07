'''
Created on Oct 19, 2015

@author: cptullio
'''
from featuring.FeatureBase import FeatureBase

class CNWFeature(FeatureBase):
    '''
    Weighted Common Neighbor by Murata
    '''
    def __repr__(self):
        return 'CNW'
    
    def getName(self):
        return 'CNW'
    

    def __init__(self):
        super(CNWFeature, self).__init__()
        self.debugar = False
        
    
    
    
    def execute(self, node1, node2, weight_index):
        print 'indice a ser usado: ', weight_index
        cnList = self.get_common_neighbors(node1, node2)
        total = 0
        
        for cn in cnList:
            denominador = ( float(self.parameter.get_weights(node1, cn)[int(weight_index)])  + float(self.parameter.get_weights(node2, cn )[int(weight_index)]))
            valor = denominador / 2
            total = total + valor
        return total
            
        