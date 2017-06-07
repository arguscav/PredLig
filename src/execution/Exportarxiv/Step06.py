'''
Created on Aug 22, 2015

@author: cptullio
Ordering Calculation
'''
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from analysing.Analyse import Analyse
from calculating.CalculateInMemory import CalculateInMemory
from calculating.VariableSelection import VariableSelection

if __name__ == '__main__':
   
    util = ParameterUtil(parameter_file = 'data/formatado/arxiv/exemplomenor/config/config.txt')
    myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, linear_combination=util.linear_combination,
                                filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None, result_random_file=util.result_random_file)

    myparams.generating_Training_Graph()
    myparams.generating_Test_Graph()
    selecao = VariableSelection(myparams.trainnigGraph)
    nodesNotLinked = selecao.readingResultsFile(util.nodes_notlinked_file)
    
    calc = CalculateInMemory(myparams, myparams.trainnigGraph)
    resultsNormalized = calc.reading_calculateResult_normalized(util.calculated_file)
    AnalyseNodesnotLinkedInFuture = Analyse.reading_analyseResult(util.result_random_file)
    topRank = Analyse.get_topRank(AnalyseNodesnotLinkedInFuture)
    orderResult = []
    if myparams.linear_combination:
        resultCombination = calc.combinate_linear(resultsNormalized)
        orderResult = calc.ordering_combinate_linear(topRank, resultCombination)
    else:
        orderResult = calc.ordering(topRank, resultsNormalized)
    FinalResult = []
    for featureOrderResult in orderResult:
        final = Analyse.AnalyseNodesInFuture(featureOrderResult, myparams.testGraph)
        FinalResult.append(final)
    Analyse.saving_analyseResult(FinalResult, util.analysed_file)
    
    
    