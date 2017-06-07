'''
Created on Aug 22, 2015

@author: cptullio
Generating TopRank
'''
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from calculating.Calculate import Calculate
from analysing.Analyse import Analyse
from formating.FormatingDataSets import FormatingDataSets

if __name__ == '__main__':
   
    util = ParameterUtil(parameter_file = 'data/formatado/duarte/1994_1999/config/configuration.txt')
    myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, 
                                filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None)


    calc = Calculate(myparams, util.nodes_notlinked_file, util.calculated_file, util.ordered_file, util.maxmincalculated_file)
    myparams.generating_Test_Graph()
    analise = Analyse(myparams, FormatingDataSets.get_abs_file_path(util.calculated_file), FormatingDataSets.get_abs_file_path(util.analysed_file) + '.random.analised.txt', calc.qtyDataCalculated)
    topRank = Analyse.getTopRank(util.analysed_file + '.random.analised.txt')
    calc.Ordering_separating_File(topRank)
    print 'Analising Files with TopRank', str(topRank)
    for OrderingFilePath in calc.getfilePathOrdered_separeted():
        analise = Analyse(myparams, OrderingFilePath, OrderingFilePath + '.analised.txt', topRank )