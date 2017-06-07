'''
Created on Aug 22, 2015

@author: cptullio
Analysing the results
'''
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from calculating.Calculate import Calculate
from analysing.Analyse import Analyse

def step07(paramFile):
    #util = ParameterUtil(parameter_file = 'data/formatado/arxiv/nowell_example_1994_1999.txt')
    util = ParameterUtil(parameter_file = paramFile)

    myparams = Parameterization(util.keyword_decay, util.lengthVertex, util.t0, util.t0_, util.t1, util.t1_, util.FeaturesChoiced, util.graph_file, util.trainnig_graph_file, util.test_graph_file, util.decay)
    calc = Calculate(myparams, util.nodes_notlinked_file, util.calculated_file, util.ordered_file, util.maxmincalculated_file)
    myparams.generating_Test_Graph()
    topRank = Analyse.getTopRank(util.analysed_file + '.random.analised.txt')
    print 'Analising Files with TopRank', str(topRank)
    for OrderingFilePath in calc.getfilePathOrdered_separeted():
        analise = Analyse(myparams, OrderingFilePath, OrderingFilePath + '.analised.txt', topRank )

if __name__ == '__main__':
    step07()
    '''
    util = ParameterUtil(parameter_file = 'data/formatado/arxiv/nowell_example_1994_1999.txt')
    myparams = Parameterization(util.keyword_decay, util.lengthVertex, util.t0, util.t0_, util.t1, util.t1_, util.FeaturesChoiced, util.graph_file, util.trainnig_graph_file, util.test_graph_file, util.decay)
    calc = Calculate(myparams, util.nodes_notlinked_file, util.calculated_file, util.ordered_file, util.maxmincalculated_file)
    myparams.generating_Test_Graph()
    topRank = Analyse.getTopRank(util.analysed_file + '.random.analised.txt')
    print 'Analising Files with TopRank', str(topRank)
    for OrderingFilePath in calc.getfilePathOrdered_separeted():
        analise = Analyse(myparams, OrderingFilePath, OrderingFilePath + '.analised.txt', topRank )
    '''