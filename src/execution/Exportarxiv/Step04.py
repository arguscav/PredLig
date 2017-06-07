'''
Created on Aug 22, 2015

@author: cptullio
Calculating All nodes not linked.
'''

from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from calculating.CalculateInMemory import CalculateInMemory
from calculating.VariableSelection import VariableSelection


if __name__ == '__main__':
    
    util = ParameterUtil(parameter_file = 'data/formatado/arxiv/exemplomenor/config/config.txt')
    #util = ParameterUtil(parameter_file = 'data/formatado/arxiv/nowell_astroph_1994_1999/config/configuration_forAG.txt')
    
    
    myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, linear_combination=util.linear_combination,
                                filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None, result_random_file=util.result_random_file)

 
    myparams.generating_Training_Graph()
    selection = VariableSelection(myparams.trainnigGraph, util.min_edges)
    
    nodesNotLinked =  selection.readingResultsFile(util.nodes_notlinked_file)
    calc = CalculateInMemory(myparams,nodesNotLinked)
    resultsofCalculation = calc.executingCalculate()
    #print resultsofCalculation
    calc.saving_calculateResult(util.calculated_file, resultsofCalculation)
    
    calc.saving_calculateResult_normalized(util.calculated_file + '_normalizated.csv', resultsofCalculation)
    result2 = calc.reading_calculateResult_normalized(util.calculated_file)
    calc.save_Max_min_file(util.maxmincalculated_file, calc.qtyDataCalculated, calc.minValueCalculated, calc.maxValueCalculated)
    print resultsofCalculation
    print result2