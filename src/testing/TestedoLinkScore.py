'''
Created on Aug 22, 2015

@author: cptullio
Analysing the results
'''
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from calculating.Calculate import Calculate
from analysing.Analyse import Analyse
from calculating.VariableSelection import VariableSelection
from formating.FormatingDataSets import FormatingDataSets
import networkx
import matplotlib

def getAllShortestPath(graph, node1, node2):
    AllDutyPaths = networkx.all_shortest_paths(graph, node1,  node2)
    AllCeanPath = []
    for dutyPath in AllDutyPaths:
        path = []
        for n in dutyPath:
            if not ('P' in n):
                path.append(n)
            
        lengthofPath = len(path)
        final = set()
        for index in range(lengthofPath-1):
            final.add( (path[index] , path[index+1]))
        if final not in AllCeanPath:    
            AllCeanPath.append(final)
    return AllCeanPath            

def getShortestPath(graph, node1, node2):
    SPpath = networkx.shortest_path(graph, node1,  node2)
    path = []
    for n in SPpath:
        if not ('P' in n):
            path.append(n)
            
    lengthofPath = len(path)
    final =[]
    for index in range(lengthofPath-1):
        final.append([path[index] , path[index+1] ] )
    return final      

if __name__ == '__main__':
    util = ParameterUtil(parameter_file = 'data/formatado/exemplomenor/config/configApenasLinkScore.txt')
    myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, 
                                filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None)

    myparams.generating_Training_Graph()
    selection = VariableSelection(myparams.trainnigGraph, util.nodes_notlinked_file,util.min_edges)
    calc = Calculate(myparams, util.nodes_notlinked_file, util.calculated_file, util.ordered_file, util.maxmincalculated_file)
    
    #networkx.draw_networkx(myparams.trainnigGraph)
    
    #matplotlib.pyplot.show()
    
    
    