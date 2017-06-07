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
    f = (float)(len(bagofWordsNode1.intersection(bagofWordsNode2)))
    x = (float)(len(bagofWordsNode1.union(bagofWordsNode2)))
    if x == 0:
        return 0
    return f/x

def get_partOfWeightCalculating(graph, database, pair, cn):
    primeiropar = sorted([str(pair[0]),str(cn)])
    segundopar = sorted([str(pair[1]),str(cn)])
    weightsA = database._pair[str(primeiropar[0])+';'+str(primeiropar[1])][0]
    weightsB = database._pair[str(segundopar[0])+';'+str(segundopar[1])][0]
    
    cnWts02 = (weightsA["TS02"] + weightsB["TS02"]) / 2
    cnWts05 = (weightsA["TS05"] + weightsB["TS05"]) / 2
    cnWts08 = (weightsA["TS08"] + weightsB["TS08"]) / 2
    
    Total_zts02 = 0
    Total_zts05 = 0
    Total_zts08 = 0
    for z in all_neighbors(graph,cn):
        parOrdernado = sorted([str(z),str(cn)])
        row = database._pair[str(parOrdernado[0])+';'+str(parOrdernado[1])]
        
        if (len(row) > 0):
            weightsZ = row[0]
            Total_zts02 = Total_zts02 + weightsZ["TS02"]
            Total_zts05 = Total_zts05 + weightsZ["TS05"]
            Total_zts08 = Total_zts08 + weightsZ["TS08"]
    
    aats02 = 1 / (numpy.log10(Total_zts02)   + 0.00001)
    aats05 = 1 / (numpy.log10(Total_zts05)   + 0.00001)
    aats08 = 1 / (numpy.log10(Total_zts08)   + 0.00001)
    
    aaWts02 = aats02 * cnWts02
    aaWts05 = aats05 * cnWts05
    aaWts08 = aats08 * cnWts08
    
    return {'cnWts02': cnWts02, 'cnWts05': cnWts05, 'cnWts08': cnWts08, 'aaWts02': aaWts02, 'aaWts05':aaWts05, 'aaWts08':aaWts08 }
    
    
    

def generateWeights(graph, weightFile, param):
    pdb = Base(weightFile)
    pdb.create('pair', 'node1', 'node2','TS02','TS05','TS08')
    pdb.create_index('pair')
    
    sortedNodes = sorted(graph.nodes())
    for node in sortedNodes:
        others = sorted(set(n for n in sortedNodes if n > node))
        for other in others:
            if graph.has_edge(node, other):
                informations = list(edge for n1, n2, edge in graph.edges([node, other], data=True) if ((n1 == node and n2 == other) or (n1 == other and n2 == node)) )
                timesofLinks = []
                for info in informations:
                    timesofLinks.append(int(info['time']))
        
               
                total_publications = len(informations)   
                k =  int(param.t0_)  - max(timesofLinks)
                decayfunction02 = (1 - 0.2) ** k
                decayfunction05 = (1 - 0.5) ** k
                decayfunction08 = (1 - 0.8) ** k
            
                pdb.insert(str(node) + ';' + str(other),node,other,(total_publications * decayfunction02) , (total_publications * decayfunction05) , (total_publications * decayfunction08) ) 
                 
    pdb.commit()            
    return pdb

def calculatingWeights(graph, nodesnotLinked, database, calculatingFile):
    pdb = Base(calculatingFile)
    pdb.create('node1', 'node2', 'cnWTS02','cnWTS05','cnWTS08', 'aaWTS02', 'aaWTS05', 'aaWTS08')
    pdb.create_index('node1', 'node2')
                
    element = 0
    qtyofNodesToProcess = len(nodesnotLinked)
    for pair in nodesnotLinked:
        element = element+1
        FormatingDataSets.printProgressofEvents(element, qtyofNodesToProcess, "Calculating features for nodes not liked: ")
        neighbors_node1 = all_neighbors(graph, pair[0])
        neighbors_node2 = all_neighbors(graph, pair[1])
        len_neihbors_node1 = len(neighbors_node1)
        len_neihbors_node2 = len(neighbors_node2)
        CommonNeigbors = neighbors_node1.intersection(neighbors_node2)
        CNWts02Feature = 0;
        CNWts05Feature = 0;
        CNWts08Feature = 0;
        AAWts02Feature = 0;
        AAWts05Feature = 0;
        AAWts08Feature = 0;
        for cn in CommonNeigbors:
            item = get_partOfWeightCalculating(graph, database, pair, cn)
            CNWts02Feature = CNWts02Feature + item['cnWts02'];
            CNWts05Feature = CNWts05Feature + item['cnWts05'];
            CNWts08Feature = CNWts08Feature + item['cnWts08'];
            AAWts02Feature = AAWts02Feature + item['aaWts02'];
            AAWts05Feature = AAWts05Feature + item['aaWts05'];
            AAWts08Feature = AAWts08Feature + item['aaWts08'];
        
            
        pdb.insert(str(pair[0]), str(pair[1]), CNWts02Feature, CNWts05Feature, CNWts08Feature, AAWts02Feature, AAWts05Feature, AAWts08Feature  )   
    pdb.commit()
    return pdb;

def get_ordering(calcDb, topRank):
    orderedResults = []
    cnWTS02 = sorted( list({ 'node1': r['node1'], 'node2': r['node2'], 'value' : r['cnWTS02']} for r in calcDb)  , key=lambda value: value['value'], reverse=True)
    cnWTS05 = sorted( list({ 'node1': r['node1'], 'node2': r['node2'], 'value' : r['cnWTS05']} for r in calcDb)  , key=lambda value: value['value'], reverse=True)
    cnWTS08 = sorted( list({ 'node1': r['node1'], 'node2': r['node2'], 'value' : r['cnWTS08']} for r in calcDb)  , key=lambda value: value['value'], reverse=True)
    aaWTS02 = sorted( list({ 'node1': r['node1'], 'node2': r['node2'], 'value' : r['aaWTS02']} for r in calcDb)  , key=lambda value: value['value'], reverse=True)
    aaWTS05 = sorted( list({ 'node1': r['node1'], 'node2': r['node2'], 'value' : r['aaWTS05']} for r in calcDb)  , key=lambda value: value['value'], reverse=True)
    aaWTS08 = sorted( list({ 'node1': r['node1'], 'node2': r['node2'], 'value' : r['aaWTS08']} for r in calcDb)  , key=lambda value: value['value'], reverse=True)
    for item in range(topRank):
        orderedResults.append({'cnWTS02' : cnWTS02[item], 'cnWTS05':cnWTS05[item], 'cnWTS08': cnWTS08[item], 'aaWTS02':aaWTS02[item], 'aaWTS05' : aaWTS05[item],'aaWTS08' : aaWTS08[item] })
    return orderedResults


def get_analyseNodesInFuture(ordering, TestGraph):
    cnWTS02 = []
    cnWTS05 = []
    cnWTS08 = []
    aaWTS02 = []
    aaWTS05 = []
    aaWTS08 = []
        
    for nodeToCheck in ordering:
        if (TestGraph.has_edge(nodeToCheck['cnWTS02']['node1'],nodeToCheck['cnWTS02']['node2'])):
            cnWTS02.append([  nodeToCheck['cnWTS02']['node1'],nodeToCheck['cnWTS02']['node2'], 1 ])
        else:
            cnWTS02.append([  nodeToCheck['cnWTS02']['node1'],nodeToCheck['cnWTS02']['node2'], 0 ])
        
        if (TestGraph.has_edge(nodeToCheck['cnWTS05']['node1'],nodeToCheck['cnWTS05']['node2'])):
            cnWTS05.append([  nodeToCheck['cnWTS05']['node1'],nodeToCheck['cnWTS05']['node2'], 1 ])
        else:
            cnWTS05.append([  nodeToCheck['cnWTS05']['node1'],nodeToCheck['cnWTS05']['node2'], 0 ])
        
        if (TestGraph.has_edge(nodeToCheck['cnWTS08']['node1'],nodeToCheck['cnWTS08']['node2'])):
            cnWTS08.append([  nodeToCheck['cnWTS08']['node1'],nodeToCheck['cnWTS08']['node2'], 1 ])
        else:
            cnWTS08.append([  nodeToCheck['cnWTS08']['node1'],nodeToCheck['cnWTS08']['node2'], 0 ])
            
        if (TestGraph.has_edge(nodeToCheck['aaWTS02']['node1'],nodeToCheck['aaWTS02']['node2'])):
            aaWTS02.append([  nodeToCheck['aaWTS02']['node1'],nodeToCheck['aaWTS02']['node2'], 1 ])
        else:
            aaWTS02.append([  nodeToCheck['aaWTS02']['node1'],nodeToCheck['aaWTS02']['node2'], 0 ])
        
        if (TestGraph.has_edge(nodeToCheck['aaWTS05']['node1'],nodeToCheck['aaWTS05']['node2'])):
            aaWTS05.append([  nodeToCheck['aaWTS05']['node1'],nodeToCheck['aaWTS05']['node2'], 1 ])
        else:
            aaWTS05.append([  nodeToCheck['aaWTS05']['node1'],nodeToCheck['aaWTS05']['node2'], 0 ])
        
        if (TestGraph.has_edge(nodeToCheck['aaWTS08']['node1'],nodeToCheck['aaWTS08']['node2'])):
            aaWTS08.append([  nodeToCheck['aaWTS08']['node1'],nodeToCheck['aaWTS08']['node2'], 1 ])
        else:
            aaWTS08.append([  nodeToCheck['aaWTS08']['node1'],nodeToCheck['aaWTS08']['node2'], 0 ])
    
    
    return {'cnWTS02' : len([result for n1,n2,result in cnWTS02 if result == 1]), 'cnWTS05' : len([result for n1,n2,result in cnWTS05 if result == 1]), 'cnWTS08' : len([result for n1,n2,result in cnWTS08 if result == 1]), 'aaWTS02' : len([result for n1,n2,result in aaWTS02 if result == 1]), 'aaWTS05' : len([result for n1,n2,result in aaWTS05 if result == 1]), 'aaWTS08' : len([result for n1,n2,result in aaWTS08 if result == 1]) }
         


def reading_Database(path):
    adb = Base(path)
    adb.open()
    return adb



    

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
    db = None
    if not os.path.exists(FormatingDataSets.get_abs_file_path(util.trainnig_graph_file + '.base.pdl')):
        db = generateWeights(myparams.trainnigGraph, FormatingDataSets.get_abs_file_path(util.trainnig_graph_file + '.base.pdl') , myparams)
    else:
        db = reading_Database(FormatingDataSets.get_abs_file_path(util.trainnig_graph_file + '.base.pdl'))
    calcDb = None
    if not os.path.exists(util.calculated_file + '.base.pdl'):
        calcDb = calculatingWeights(myparams.trainnigGraph, nodeSelection.nodesNotLinked, db, util.calculated_file + '.base.pdl')
    else:
        calcDb = reading_Database(util.calculated_file + '.base.pdl')
        
    ordering = get_ordering(calcDb, len(nodeSelection.eNeW))
    
    result = get_analyseNodesInFuture(ordering, myparams.testGraph)
    
    resultFile.write(repr(result))
    
    resultFile.write("\n")
#        
    resultFile.write("Authors\tArticles\tCollaborations\tAuthors\tEold\tEnew\n")
    resultFile.write( str(myparams.get_nodes(myparams.trainnigGraph))+ "\t" + str(myparams.get_edges(myparams.trainnigGraph)) + "\t\t" + str(len(nodeSelection.get_NowellColaboration())*2)+ "\t\t" + str(len(nodeSelection.nodes)) + "\t" + str(len(nodeSelection.eOld))+"\t" + str(len(nodeSelection.eNeW)))
     
 
    resultFile.write("\n")

    resultFile.write("Fim da Operacao\n")
    resultFile.write(str(datetime.datetime.now()))
    
    resultFile.close()

def grqc():
    configFile = 'data/configuration/arxiv/grqc/WeightedGraph/config_NOWELLTS.txt'
    execution(configFile)

def astroph():
    configFile = 'data/configuration/arxiv/astroph/WeightedGraph/config_NOWELLTS.txt'
    execution(configFile)

def condmat():
    configFile = 'data/configuration/arxiv/condmat/WeightedGraph/config_NOWELLTS.txt'
    execution(configFile)
    
def hepth():
    configFile = 'data/configuration/arxiv/hepth/WeightedGraph/config_NOWELLTS.txt'
    execution(configFile)

def hepph():
    configFile = 'data/configuration/arxiv/hepph/WeightedGraph/config_NOWELLTS.txt'
    execution(configFile)

if __name__ == '__main__':
    grqc()
    astroph()
    hepth()
    hepph()
    condmat()
    
    