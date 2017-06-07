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



def saving_files_calculting_input(filename, data):
    
    output = open(filename  , 'w')
    output.write('no1,no2,IntensityNode1,IntensityNode2,Similarity,AgeNo1,AgeNo2\n')
    for item in data:
        output.write(repr(item['no1']))
        output.write(',')
        output.write(repr(item['no2']))
        output.write(',')
        
        output.write(repr(item['intensityno1']))
        output.write(',')
        
        output.write(repr(item['intensityno2']))
        output.write(',')
        
        output.write(repr(item['similarity']))
        output.write(',')
        
        output.write(repr(item['ageno1']))
        output.write(',')
        
        output.write(repr(item['ageno2']))
        output.write('\n')
        
        
    output.close()
    output.close()

def save_file(filename, data):
    
    output = open(filename  , 'w')
    output.write(repr(data))
    output.close()
    
def get_TotalSucess(analise):
    Sucess =  len(  list([n1,n2] for n1,n2,result in analise if result ==1 ) )
    return {'sucess':Sucess}
    
    
def AnalyseNodesInFuture(ordering, TestGraph):
    Analise = []
    for nodeToCheck in ordering:
        if (TestGraph.has_edge(nodeToCheck['no1'],nodeToCheck['no2'])):
            Analise.append([  nodeToCheck['no1'],nodeToCheck['no2'], 1 ])
        else:
            Analise.append([  nodeToCheck['no1'],nodeToCheck['no2'], 0 ])
    return Analise

def all_neighbors(graph, node):
    return set(networkx.all_neighbors(graph, node))
    
def get_common_neighbors(graph, node1, node2):
    neighbors_node_1 = all_neighbors(node1)
    neighbors_node_2 = all_neighbors(node2)
    return neighbors_node_1.intersection(neighbors_node_2)    
    
def get_ObjectsofLinks(graph, node1, node2):
    T3 = list(edge for n1, n2, edge in graph.edges([node1, node2], data=True) if ((n1 == node1 and n2 == node2) or (n1 == node2 and n2 == node1)) )
    return  T3
    
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
    
    result = []
                
    element = 0
    qtyofNodesToProcess = len(nodesnotLinked)
    for pair in nodesnotLinked:
        #element = element+1
        #FormatingDataSets.printProgressofEvents(element, qtyofNodesToProcess, "Calculating features for nodes not liked: ")
        neighbors_node1 = all_neighbors(graph, pair[0])
        neighbors_node2 = all_neighbors(graph, pair[1])
        len_neihbors_node1 = len(neighbors_node1)
        len_neihbors_node2 = len(neighbors_node2)
        CommonNeigbors = neighbors_node1.intersection(neighbors_node2)
        resultValue = 0
        
        for cn in CommonNeigbors:
            
            infoNode1 = list(edge for n1, n2, edge in graph.edges([ pair[0], cn], data=True) if ((n1 ==  pair[0] and n2 == cn) or (n1 == cn and n2 == pair[0])) )
            infoNode2 = list(edge for n1, n2, edge in graph.edges([pair[1], cn], data=True) if ((n1 ==  pair[1] and n2 == cn) or (n1 == cn and n2 == pair[1])) )
            
            IntensityNodeAC = len(infoNode1)
            IntensityNodeBC = len(infoNode2)
            
            MaxTimeNodeAC =  max(info['time'] for info in infoNode1 if 1==1)
            MaxTimeNodeBC =  max(info['time'] for info in infoNode2 if 1==1)
            
            bagofWordsNode1 =  list(info['keywords'] for info in infoNode1 if 1==1)
            bagofWordsNode2 =  list(info['keywords'] for info in infoNode2 if 1==1)
            
            Similarities = get_jacard_domain(bagofWordsNode1, bagofWordsNode2)*100
            
            data = FuzzyCalculation(IntensityNodeAC, IntensityNodeBC, Similarities, abs(params.t0_ - MaxTimeNodeAC),  abs(params.t0_ - MaxTimeNodeAC))
            
            if (resultValue < data.grau_potencial_ligacao):
                resultValue = data.grau_potencial_ligacao
        
        result.append({'no1': pair[0], 'no2': pair[1], 'result': resultValue  })
    return result


def execution(configFile):
    
    #DEFINE THE FILE THAT WILL KEEP THE RESULT DATA
    resultFile = open(FormatingDataSets.get_abs_file_path(configFile + 'core03.txt'), 'w')
    
    resultFile.write("Inicio da operacao\n")
    resultFile.write(str(datetime.datetime.now()))
    resultFile.write("\n")

    
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
    data = calculatingInputToFuzzy(myparams.trainnigGraph,nodeSelection.nodesNotLinked,  myparams)
    dataSorted = sorted(data, key=lambda value: value['result'], reverse=True)
    
    topRank = len(nodeSelection.eNeW)
    totalCalculated = len(dataSorted)
    dataToAnalysed = []
    if (topRank >= totalCalculated):
        for item in range(totalCalculated):
            dataToAnalysed.append({'no1':  dataSorted[item]['no1'], 'no2': dataSorted[item]['no2'], 'result':  dataSorted[item]['result'] })
    else:
        for item in range(topRank):
            dataToAnalysed.append({'no1':  dataSorted[item]['no1'], 'no2': dataSorted[item]['no2'], 'result':  dataSorted[item]['result'] })
            
    
    analise = AnalyseNodesInFuture(dataToAnalysed, myparams.testGraph)
    
    resultFile.write( repr(get_TotalSucess(analise)) )   
    
    resultFile.write("\n")
#        
    resultFile.write("Authors\tArticles\tCollaborations\tAuthors\tEold\tEnew\n")
    resultFile.write( str(myparams.get_nodes(myparams.trainnigGraph))+ "\t" + str(myparams.get_edges(myparams.trainnigGraph)) + "\t\t" + str(len(nodeSelection.get_NowellColaboration())*2)+ "\t\t" + str(len(nodeSelection.nodes)) + "\t" + str(len(nodeSelection.eOld))+"\t" + str(len(nodeSelection.eNeW)))
     
 
    resultFile.write("\n")

    resultFile.write("Fim da Operacao\n")
    resultFile.write(str(datetime.datetime.now()))
    
    resultFile.close()

def grqc():
    #configFile = 'data/configuration/arxiv/grqc/WeightedGraph/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/grqc/WeightedGraph/config_Arxiv99.txt'
    
    configFile = 'data/configuration/arxiv/grqc/fuzzylogic/config_NOWELLTSRich.txt'
    execution(configFile)

def astroph():
    #configFile = 'data/configuration/arxiv/astroph/WeightedGraph/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/astroph/WeightedGraph/config_Arxiv99.txt'
    
    configFile = 'data/configuration/arxiv/astroph/fuzzylogic/config_NOWELLTSRich.txt'
    execution(configFile)

def condmat():
    #configFile = 'data/configuration/arxiv/condmat/WeightedGraph/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/condmat/WeightedGraph/config_Arxiv99.txt'
    
    configFile = 'data/configuration/arxiv/condmat/fuzzylogic/config_NOWELLTSRich.txt'
    execution(configFile)
    
def hepth():
    #configFile = 'data/configuration/arxiv/hepth/WeightedGraph/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/hepth/WeightedGraph/config_Arxiv99.txt'
    
    configFile = 'data/configuration/arxiv/hepth/fuzzylogic/config_NOWELLTSRich.txt'
    execution(configFile)

def hepph():
    #configFile = 'data/configuration/arxiv/hepph/WeightedGraph/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/hepph/WeightedGraph/config_Arxiv99.txt'
    
    configFile = 'data/configuration/arxiv/hepph/fuzzylogic/config_NOWELLTSRich.txt'
    execution(configFile)

if __name__ == '__main__':
    grqc()
    #astroph()
    #hepth()
    #hepph()
    #condmat()
    
    