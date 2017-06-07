'''
Created on Aug 22, 2015

@author: cptullio
Process of partition the graph in two for training and for test

'''
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization

if __name__ == '__main__':
    util = ParameterUtil(parameter_file = 'data/formatado/duarte/1994_1999/config/configuration.txt')
    myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, 
                                filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None)

    
    myparams.generating_Training_Graph()
    myparams.generating_Test_Graph()
    