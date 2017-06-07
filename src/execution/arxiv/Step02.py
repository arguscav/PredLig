'''
Created on Aug 22, 2015

@author: cptullio
Process of partition the graph in two for training and for test

'''
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization

def step02(paramFile):
    #util = ParameterUtil(parameter_file = 'data/formatado/arxiv/nowell_example_1994_1999.txt')
    util = ParameterUtil(parameter_file = paramFile)
    myparams = Parameterization(util.keyword_decay, util.lengthVertex, util.t0, util.t0_, util.t1, util.t1_, util.FeaturesChoiced, util.graph_file, util.trainnig_graph_file, util.test_graph_file, util.decay)
    myparams.generating_Training_Graph()
    myparams.generating_Test_Graph()

if __name__ == '__main__':
    step02()
    '''
    util = ParameterUtil(parameter_file = 'data/formatado/arxiv/nowell_example_1994_1999.txt')
    myparams = Parameterization(util.keyword_decay, util.lengthVertex, util.t0, util.t0_, util.t1, util.t1_, util.FeaturesChoiced, util.graph_file, util.trainnig_graph_file, util.test_graph_file, util.decay)
    myparams.generating_Training_Graph()
    myparams.generating_Test_Graph()
    '''
    
