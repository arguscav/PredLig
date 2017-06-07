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
from calculating.VariableSelection import VariableSelection


if __name__ == '__main__':
   
    util = ParameterUtil(parameter_file = 'data/formatado/arxiv/exemplomenor/config/config.txt')
    myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, linear_combination=util.linear_combination,
                                filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None, result_random_file=util.result_random_file)

    myparams.generating_Training_Graph()
    myparams.generating_Test_Graph()
    selection = VariableSelection(myparams.trainnigGraph)
    nodesNotLinked = selection.readingResultsFile(util.nodes_notlinked_file)
    resultsRank = Analyse.AnalyseNodesInFuture(nodesNotLinked, myparams.testGraph)
    Analyse.saving_analyseResult(resultsRank, util.result_random_file)
    print resultsRank
    print Analyse.reading_analyseResult(util.result_random_file)
    