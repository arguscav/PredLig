'''
Created on Aug 22, 2015

@author: cptullio
Analysing the results
'''
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from analysing.Analyse import Analyse
from calculating.VariableSelection import VariableSelection
from formating.FormatingDataSets import FormatingDataSets
import networkx
import matplotlib.pyplot as plt
from calculating.CalculateInMemory import CalculateInMemory

if __name__ == '__main__':
    
    
    #plt.show()
    #util = ParameterUtil(parameter_file = 'data/formatado/arxiv/nowell_astroph_1994_1999/AllExecutionScores/config.txt')
    util = ParameterUtil(parameter_file = 'data/formatado/arxiv/exemplomenor/config/config.txt')
    
    myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, linear_combination=util.linear_combination,
                                filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None, result_random_file=util.result_random_file)

    myparams.generating_Training_Graph()
    #myparams.generating_Test_Graph()
    
    selection = VariableSelection(myparams.trainnigGraph, util.min_edges)
    nodesNotLinked = selection.get_pair_nodes_not_linked()
    selection.saveResults(util.nodes_notlinked_file, nodesNotLinked)
    
    #dado =  selection.readingResultsFile(util.nodes_notlinked_file)
    #print dado[1]
    #calc = CalculateInMemory(myparams, nodesNotLinked)
    #resultsCalculate = calc.executingCalculate()
    #resultados = []
    #orderDataMetrica0 = sorted(resultsCalculate, key=lambda value: value[0][0], reverse=True)
    #orderDataMetrica1 = sorted(resultsCalculate, key=lambda value: value[0][5], reverse=True)
    
    #for result in orderDataMetrica1:
        
    #    metricas = result[0]
    #    no1 = result[1]
    #    no2 = result[2]
    #    print metricas, no1, no2