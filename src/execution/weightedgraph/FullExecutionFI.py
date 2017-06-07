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

def get_partOfWeightCalculating(graph, database, pair, cn):
    primeiropar = sorted([str(pair[0]),str(cn)])
    segundopar = sorted([str(pair[1]),str(cn)])
    weightsA = database._pair[str(primeiropar[0])+';'+str(primeiropar[1])][0]
    weightsB = database._pair[str(segundopar[0])+';'+str(segundopar[1])][0]
    
    WCN = (weightsA["FI"] + weightsB["FI"]) / 2
    
    
    Total_zts02 = 0
    #Total_zjc = 0
    for z in all_neighbors(graph,cn):
        parOrdernado = sorted([str(z),str(cn)])
        row = database._pair[str(parOrdernado[0])+';'+str(parOrdernado[1])]
        
        if (len(row) > 0):
            weightsZ = row[0]
            Total_zts02 = Total_zts02 + weightsZ["FI"]
            #Total_zjc = Total_zjc + weightsZ["JC"]
            
    
    _WAA = 1 / (numpy.log10(Total_zts02)   + 0.00001)
    
    WAA = _WAA * WCN
    
    return {'WCN': WCN, 'WAA': WAA }
    
    
    

def generateWeights(graph, weightFile, param):
    pdb = Base(weightFile)
    pdb.create('pair', 'node1', 'node2','FI')
    pdb.create_index('pair')
    
    sortedNodes = sorted(graph.nodes())
    for node in sortedNodes:
        others = sorted(set(n for n in sortedNodes if n > node))
        for other in others:
            if graph.has_edge(node, other):
                informations = list(edge for n1, n2, edge in graph.edges([node, other], data=True) if ((n1 == node and n2 == other) or (n1 == other and n2 == node)) )
                        
                total_publications = len(informations)   
                pdb.insert(str(node) + ';' + str(other),node,other, total_publications ) 
                 
    pdb.commit()            
    return pdb

def calculatingWeights(graph, nodesnotLinked, database, calculatingFile):
    pdb = Base(calculatingFile)
    pdb.create('node1', 'node2', 'WCNFI','WAAFI')
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
        WCNFI = 0;
        WAAFI = 0;
        
        for cn in CommonNeigbors:
            item = get_partOfWeightCalculating(graph, database, pair, cn)
            WCNFI = WCNFI + item['WCN'];
            WAAFI = WAAFI + item['WAA'];
        pdb.insert(str(pair[0]), str(pair[1]), WCNFI, WAAFI )   
    pdb.commit()
    return pdb;


def generate_finalResult(order,topRank, TestGraph, FileNameResult ):
    pdb = Base(FileNameResult)
    pdb.create('node1', 'node2', 'value', 'sucesso','topRank')
    pdb.create_index('node1', 'node2')
 
    indice = 0 
    for nodeToCheck in order:
        indice = indice+1
        isTopRank = (indice <= topRank)
        if (TestGraph.has_edge(nodeToCheck['node1'],nodeToCheck['node2'])):
            pdb.insert(str(nodeToCheck['node1']), nodeToCheck['node2'],nodeToCheck['value'] , True, isTopRank  ) 
        else:   
            pdb.insert(str(nodeToCheck['node1']), nodeToCheck['node2'],nodeToCheck['value'] , False, isTopRank  ) 
    
    pdb.commit()
    return pdb
    

def get_results(db, MethodName):
    VP = len(list( r for r in db if (r['sucesso'] == True and r['topRank'] == True ) ))
    VN = len(list(r for r in db if (r['sucesso'] == False and r['topRank'] == True )))
    FP = len(list(r for r in db if (r['sucesso'] == True and r['topRank'] == False)))
    FN = len(list(r for r in db if (r['sucesso'] == False and r['topRank'] == False)))
    return {'Method': MethodName, 'VP': VP, 'VN': VN, 'FP': FP, 'FN': FN }

def get_analyseNodesInFuture(calcDb, topRank, TestGraph, util):
    
    result = []
    WCNFI_ORDERED = sorted( list({ 'node1': r['node1'], 'node2': r['node2'], 'value' : r['WCNFI']} for r in calcDb)  , key=lambda value: value['value'], reverse=True)
    WCNFIBD = None
    if not os.path.exists(FormatingDataSets.get_abs_file_path(util.calculated_file + '.WCNFI.base.pdl')):
        WCNFIBD = generate_finalResult(WCNFI_ORDERED, topRank, TestGraph, FormatingDataSets.get_abs_file_path(util.calculated_file + '.WCNFI.base.pdl'))
    
    else:
        WCNFIBD = reading_Database(FormatingDataSets.get_abs_file_path(util.calculated_file + '.WCNFI.base.pdl'))
    
    result.append(get_results(WCNFIBD, 'WCNFI'))
    
    
    WAAFI_ORDERED = sorted( list({ 'node1': r['node1'], 'node2': r['node2'], 'value' : r['WAAFI']} for r in calcDb)  , key=lambda value: value['value'], reverse=True)
    WAAFIBD = None
    if not os.path.exists(FormatingDataSets.get_abs_file_path(util.calculated_file + '.WAAFI.base.pdl')):
        WAAFIBD = generate_finalResult(WAAFI_ORDERED, topRank, TestGraph, FormatingDataSets.get_abs_file_path(util.calculated_file + '.WAAFI.base.pdl'))
    
    else:
        WAAFIBD = reading_Database(FormatingDataSets.get_abs_file_path(util.calculated_file + '.WAAFI.base.pdl'))
    
    result.append(get_results(WAAFIBD, 'WAAFI'))
    return result    
    

def reading_Database(path):
    adb = Base(path)
    adb.open()
    return adb



    

def execution(configFile):
   
    
    #DEFINE THE FILE THAT WILL KEEP THE RESULT DATA
    resultFile = open(FormatingDataSets.get_abs_file_path(configFile + 'FI.txt'), 'w')
    
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
    if not os.path.exists(FormatingDataSets.get_abs_file_path(util.calculated_file + '.base.pdl')):
        calcDb = calculatingWeights(myparams.trainnigGraph, nodeSelection.nodesNotLinked, db, FormatingDataSets.get_abs_file_path(util.calculated_file) + '.base.pdl')
    else:
        calcDb = reading_Database(FormatingDataSets.get_abs_file_path(util.calculated_file + '.base.pdl'))
        
    topRank = len(nodeSelection.eNeW)
    
    result = get_analyseNodesInFuture(calcDb, topRank, myparams.testGraph, util)
    
    for r in result:
        resultFile.write('Metodo: ')
        resultFile.write(r['Method'])
        resultFile.write("\n")
        resultFile.write('VP: ')
        resultFile.write(repr(r['VP']))
        resultFile.write("\n")
   
        resultFile.write('VN: ')
        resultFile.write(repr(r['VN']))
        resultFile.write("\n")
   
        resultFile.write('FP: ')
        resultFile.write(repr(r['FP']))
        resultFile.write("\n")
   
        resultFile.write('FN: ')
        resultFile.write(repr(r['FN']))
        resultFile.write("\n")
   
        
       
    resultFile.write("\n")
        
    resultFile.write("Authors\tArticles\tCollaborations\tAuthors\tEold\tEnew\n")
    resultFile.write( str(myparams.get_nodes(myparams.trainnigGraph))+ "\t" + str(myparams.get_edges(myparams.trainnigGraph)) + "\t\t" + str(len(nodeSelection.get_NowellColaboration())*2)+ "\t\t" + str(len(nodeSelection.nodes)) + "\t" + str(len(nodeSelection.eOld))+"\t" + str(len(nodeSelection.eNeW)))
     
 
    resultFile.write("\n")

    resultFile.write("Fim da Operacao\n")
    resultFile.write(str(datetime.datetime.now()))
    
    resultFile.close()

def grqc():
    #configFile = 'data/configuration/arxiv/grqc/WeightedGraph/config_Arxiv05.txt'
    configFile = 'data/configuration/arxiv/grqc/WeightedGraph/config_Arxiv99.txt'
    
    #configFile = 'data/configuration/arxiv/grqc/WeightedGraph/config_NOWELLTSRich.txt'
    execution(configFile)

def astroph():
    #configFile = 'data/configuration/arxiv/astroph/WeightedGraph/config_Arxiv05.txt'
    configFile = 'data/configuration/arxiv/astroph/WeightedGraph/config_Arxiv99.txt'
    
    #configFile = 'data/configuration/arxiv/astroph/WeightedGraph/config_NOWELLTSRich.txt'
    execution(configFile)

def condmat():
    #configFile = 'data/configuration/arxiv/condmat/WeightedGraph/config_Arxiv05.txt'
    configFile = 'data/configuration/arxiv/condmat/WeightedGraph/config_Arxiv99.txt'
    
    #configFile = 'data/configuration/arxiv/condmat/WeightedGraph/config_NOWELLTSRich.txt'
    execution(configFile)
    
def hepth():
    #configFile = 'data/configuration/arxiv/hepth/WeightedGraph/config_Arxiv05.txt'
    configFile = 'data/configuration/arxiv/hepth/WeightedGraph/config_Arxiv99.txt'
    
    #configFile = 'data/configuration/arxiv/hepth/WeightedGraph/config_NOWELLTSRich.txt'
    execution(configFile)

def hepph():
    #configFile = 'data/configuration/arxiv/hepph/WeightedGraph/config_Arxiv05.txt'
    configFile = 'data/configuration/arxiv/hepph/WeightedGraph/config_Arxiv99.txt'
    
    #configFile = 'data/configuration/arxiv/hepph/WeightedGraph/config_NOWELLTSRich.txt'
    execution(configFile)


def mas05():
    configFile = 'data/configuration/arxiv/duarte/WeightedGraph/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/hepph/WeightedGraph/config_Arxiv99.txt'
    
    #configFile = 'data/configuration/arxiv/hepph/WeightedGraph/config_NOWELLTSRich.txt'
    execution(configFile)


def mas99():
    configFile = 'data/configuration/arxiv/duarte/WeightedGraph/config_Arxiv99.txt'
    #configFile = 'data/configuration/arxiv/hepph/WeightedGraph/config_Arxiv99.txt'
    
    #configFile = 'data/configuration/arxiv/hepph/WeightedGraph/config_NOWELLTSRich.txt'
    execution(configFile)

def grqc05():
    configFile = 'data/configuration/arxiv/grqc/WeightedGraph/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/grqc/WeightedGraph/config_Arxiv99.txt'
    
    #configFile = 'data/configuration/arxiv/grqc/WeightedGraph/config_NOWELLTSRich.txt'
    execution(configFile)

def astroph05():
    configFile = 'data/configuration/arxiv/astroph/WeightedGraph/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/astroph/WeightedGraph/config_Arxiv99.txt'
    
    #configFile = 'data/configuration/arxiv/astroph/WeightedGraph/config_NOWELLTSRich.txt'
    execution(configFile)

def condmat05():
    configFile = 'data/configuration/arxiv/condmat/WeightedGraph/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/condmat/WeightedGraph/config_Arxiv99.txt'
    
    #configFile = 'data/configuration/arxiv/condmat/WeightedGraph/config_NOWELLTSRich.txt'
    execution(configFile)
    
def hepth05():
    configFile = 'data/configuration/arxiv/hepth/WeightedGraph/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/hepth/WeightedGraph/config_Arxiv99.txt'
    
    #configFile = 'data/configuration/arxiv/hepth/WeightedGraph/config_NOWELLTSRich.txt'
    execution(configFile)

def hepph05():
    configFile = 'data/configuration/arxiv/hepph/WeightedGraph/config_Arxiv05.txt'
    #configFile = 'data/configuration/arxiv/hepph/WeightedGraph/config_Arxiv99.txt'
    
    #configFile = 'data/configuration/arxiv/hepph/WeightedGraph/config_NOWELLTSRich.txt'
    execution(configFile)



if __name__ == '__main__':
    #grqc()
    #grqc05()
    #astroph()
    #hepth()
    #hepph()
    condmat()
    astroph05()
    hepth05()
    hepph05()
    condmat05()
    
       
    