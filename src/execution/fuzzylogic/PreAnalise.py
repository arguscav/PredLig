'''
Created on 19 de abr de 2016

@author: CarlosPM
'''
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from formating.FormatingDataSets import FormatingDataSets
from calculating.CalculateInMemory import CalculateInMemory
from analysing.Analyse import Analyse
from calculating.VariableSelection import VariableSelection
import networkx
import datetime
from calculating.NodeSelection import NodeSelection
from calculating.CalculatingTogetherOnlyNowell import CalculatingTogetherOnlyNowell
from pydblite import Base
import numpy
import os
from calculating.FuzzyCalculation import FuzzyCalculation


def saving_analise(data, titulo, grafo):
    output = open( grafo + '_.' + titulo + '.csv'  , 'w')
    output.write(titulo+'\n')
    for item in data:
        output.write(repr(item))
        output.write('\n')
    output.close()
    

def all_neighbors(graph, node):
    return set(networkx.all_neighbors(graph, node))
    
    
    
def get_jacard_domain(bagofWordsNode1, bagofWordsNode2):
    wN1 = set()
    for n1 in bagofWordsNode1:
        for n11 in n1:
            wN1.add(n11)
    
    wN2 = set()
    for n2 in bagofWordsNode2:
        for n22 in n2:
            wN2.add(n22)
    
       
    f = (float)(len(wN1.intersection(wN2)))
    x = (float)(len(wN1.union(wN2)))
    if x == 0:
        return 0
    return f/x


def calculatingInputToFuzzy(graph, nodesnotLinked,  params):
    
    intensity = set()
    ages = set()
    similarities = set()            
    
    for pair in nodesnotLinked:
        neighbors_node1 = all_neighbors(graph, pair[0])
        neighbors_node2 = all_neighbors(graph, pair[1])
        len_neihbors_node1 = len(neighbors_node1)
        len_neihbors_node2 = len(neighbors_node2)
        CommonNeigbors = neighbors_node1.intersection(neighbors_node2)
        
        for cn in CommonNeigbors:
            
            infoNode1 = list(edge for n1, n2, edge in graph.edges([ pair[0], cn], data=True) if ((n1 ==  pair[0] and n2 == cn) or (n1 == cn and n2 == pair[0])) )
            infoNode2 = list(edge for n1, n2, edge in graph.edges([pair[1], cn], data=True) if ((n1 ==  pair[1] and n2 == cn) or (n1 == cn and n2 == pair[1])) )
            
            intensity.add(len(infoNode1))
            intensity.add(len(infoNode2))
            
            MaxTimeNodeAC =  max(info['time'] for info in infoNode1 if 1==1)
            MaxTimeNodeBC =  max(info['time'] for info in infoNode2 if 1==1)
            
            bagofWordsNode1 =  list(info['keywords'] for info in infoNode1 if 1==1)
            bagofWordsNode2 =  list(info['keywords'] for info in infoNode2 if 1==1)
            
            similarities.add(get_jacard_domain(bagofWordsNode1, bagofWordsNode2)*100)
            ages.add( abs(params.t0_ - MaxTimeNodeAC)  )
            ages.add( abs(params.t0_ - MaxTimeNodeBC)  )
            
            
    saving_analise(ages, 'ages', params.filePathGraph)
    saving_analise(intensity, 'intensity', params.filePathGraph)
    saving_analise(similarities, 'similarities', params.filePathGraph)
    
        

def execution(configFile):
    
    #READING THE CONFIG FILE
    util = ParameterUtil(parameter_file = configFile)
    #CREATING PARAMETRIZATION OBJECT WITH THE INFORMATIONS OF THE CONFIG FILE.
    myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, linear_combination=util.linear_combination,
                                filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None, result_random_file=util.result_random_file)

    #GENERATING TRAINNING GRAPH BASED ON CONFIG FILE T0 AND T0_
    myparams.generating_Training_Graph()
      
    #GENERATING TEST GRAPH BASED ON CONcvb FIG FILE T1 AND T1_
    myparams.generating_Test_Graph()
    
    nodeSelection = NodeSelection(myparams.trainnigGraph, myparams.testGraph, util)
    #if not os.path.exists(FormatingDataSets.get_abs_file_path(util.trainnig_graph_file + '.fuzzyinputy.txt')):
    calculatingInputToFuzzy(myparams.trainnigGraph,nodeSelection.nodesNotLinked,  myparams)
        
 
    
def grqc():
    #configFile = 'data/configuration/arxiv/grqc/MetricaTemporal/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/grqc/MetricaTemporal/config_Arxiv99.txt'
    
    configFile = 'data/configuration/arxiv/grqc/MetricaTemporal/config_NOWELLTSRich.txt'
    execution(configFile)

def astroph():
    #configFile = 'data/configuration/arxiv/astroph/MetricaTemporal/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/astroph/MetricaTemporal/config_Arxiv99.txt'
    
    configFile = 'data/configuration/arxiv/astroph/MetricaTemporal/config_NOWELLTSRich.txt'
    execution(configFile)

def condmat():
    #configFile = 'data/configuration/arxiv/condmat/MetricaTemporal/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/condmat/MetricaTemporal/config_Arxiv99.txt'
    
    configFile = 'data/configuration/arxiv/condmat/MetricaTemporal/config_NOWELLTSRich.txt'
    execution(configFile)
    
def hepth():
    #configFile = 'data/configuration/arxiv/hepth/MetricaTemporal/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/hepth/MetricaTemporal/config_Arxiv99.txt'
    
    configFile = 'data/configuration/arxiv/hepth/MetricaTemporal/config_NOWELLTSRich.txt'
    execution(configFile)

def hepph():
    #configFile = 'data/configuration/arxiv/hepph/MetricaTemporal/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/hepph/MetricaTemporal/config_Arxiv99.txt'
    
    configFile = 'data/configuration/arxiv/hepph/MetricaTemporal/config_NOWELLTSRich.txt'
    execution(configFile)

if __name__ == '__main__':
    grqc()
    astroph()
    hepth()
    hepph()
    condmat()
    
    