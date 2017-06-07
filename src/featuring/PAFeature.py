'''
Created on Jun 16, 2015

@author: cptullio
'''
from featuring.FeatureBase import FeatureBase

class PAFeature(FeatureBase):
    '''
    Preference Attachment
    '''

    def __repr__(self):
        return 'pa'
    
    def getName(self):
        return 'pa' 
    
    def __init__(self):
        super(PAFeature, self).__init__()

    def execute(self, node1, node2):
        neighbors_node1 = self.all_neighbors(node1)
        neighbors_node2 = self.all_neighbors(node2)
        return len(neighbors_node1) * len(neighbors_node2)
    