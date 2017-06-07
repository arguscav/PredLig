'''
Created on Oct 4, 2015

@author: cptullio
'''
from featuring.FeatureBase import FeatureBase
import numpy

class WAAFeature(FeatureBase):
    '''
    Weighted Adamic-Adar by Linyuan Lu and Tao
    '''
    def __repr__(self):
        return 'WAA'
    
    def getName(self):
        return 'WAA'

    def __init__(self):
        super(WAAFeature, self).__init__()
        self.debugar = False
        
    
    
    
    def execute(self, node1, node2, weight_index):
        print 'indice a ser usado: ', weight_index
        cnList = self.get_common_neighbors(node1, node2)
        total = 0
        
        for cn in cnList:
            numerador =  ( float(self.parameter.get_weights(node1, cn)[int(weight_index)])  + float(self.parameter.get_weights(node2, cn )[int(weight_index)]))
            Total_z = 0
            for z in self.all_node_neighbors(cn):
                Total_z = Total_z + float(self.parameter.get_weights(z, cn)[int(weight_index)]) 
            denominador = (numpy.log10(1+Total_z)   + 0.00001)
            total = total + ( numerador / denominador   )
            
            
        return total
            
        