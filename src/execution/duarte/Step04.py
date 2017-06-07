'''
Created on Aug 22, 2015

@author: cptullio
Selecting all Nodes that will be calculated.
'''

from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from calculating.Calculate import Calculate
import networkx
from matplotlib import pyplot

if __name__ == '__main__':
    #util = ParameterUtil(parameter_file = 'data/formatado/arxiv/exemplomenor/config/configuration_weights.txt')
    util = ParameterUtil(parameter_file = 'data/formatado/duarte/1994_1999/config/configuration.txt')
    myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, 
                                filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None)

    myparams.generating_Training_Graph()
 
    calc = Calculate(myparams, util.nodes_notlinked_file, util.calculated_file, util.ordered_file, util.maxmincalculated_file)
    calc.Separating_calculateFile()
    #networkx.networkx.draw_networkx(myparams.trainnigGraph)  # networkx draw()
    #pyplot.draw()  # pyplot draw()
    #pyplot.show()