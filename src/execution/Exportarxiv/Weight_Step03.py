'''
Created on 30 de set de 2015

@author: CarlosPM
'''
from formating.FormatingDataSets import FormatingDataSets
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from analysing.Analyse import Analyse
from calculating.CalculateWeights import CalculateWeights

if __name__ == '__main__':
    util = ParameterUtil(parameter_file = 'data/formatado/duarte/1994_1999/config/configuration_weights.txt')
       
    
    myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, 
                                filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None)

    myparams.generating_Test_Graph()
    calc = CalculateWeights(preparedParameter = myparams, filepathNodesNotLinked = util.nodes_notlinked_file, filepathResult = util.calculated_file, filePathOrdered = util.ordered_file, filepathMaxMinCalculated = util.maxmincalculated_file)
    calc.Separating_calculateFile()
    analise = Analyse(myparams, FormatingDataSets.get_abs_file_path(util.calculated_file), FormatingDataSets.get_abs_file_path(util.analysed_file) + '.random.analised.txt', calc.qtyDataCalculated)
    
    topRank = Analyse.getTopRank(util.analysed_file + '.random.analised.txt')
    calc.Ordering_separating_File(topRank)
    for OrderingFilePath in calc.getfilePathOrdered_separeted():
        analise = Analyse(myparams, OrderingFilePath, OrderingFilePath + '.analised.txt', topRank )