'''
Created on 19 de abr de 2016

@author: CarlosPM
'''
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from formating.FormatingDataSets import FormatingDataSets
import networkx
import datetime
from calculating.NodeSelection import NodeSelection
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
    WCN = []
    WCN.append( (weightsA["FTI01"] + weightsB["FTI01"]) / 2)
    WCN.append((weightsA["FTI02"] + weightsB["FTI02"]) / 2)
    WCN.append((weightsA["FTI03"] + weightsB["FTI03"]) / 2)
    WCN.append((weightsA["FTI04"] + weightsB["FTI04"]) / 2)
    WCN.append((weightsA["FTI05"] + weightsB["FTI05"]) / 2)
    WCN.append((weightsA["FTI06"] + weightsB["FTI06"]) / 2)
    WCN.append((weightsA["FTI07"] + weightsB["FTI07"]) / 2)
    WCN.append((weightsA["FTI08"] + weightsB["FTI08"]) / 2)
    WCN.append((weightsA["FTI09"] + weightsB["FTI09"]) / 2)
    
    
    TOTALZFTI01 = 0
    TOTALZFTI02 = 0
    TOTALZFTI03 = 0
    TOTALZFTI04 = 0
    TOTALZFTI05 = 0
    TOTALZFTI06 = 0
    TOTALZFTI07 = 0
    TOTALZFTI08 = 0
    TOTALZFTI09 = 0
    
    for z in all_neighbors(graph,cn):
        parOrdernado = sorted([str(z),str(cn)])
        row = database._pair[str(parOrdernado[0])+';'+str(parOrdernado[1])]
        
        if (len(row) > 0):
            weightsZ = row[0]
            TOTALZFTI01 = TOTALZFTI01 + weightsZ["FTI01"]
            TOTALZFTI02 = TOTALZFTI02 + weightsZ["FTI02"]
            TOTALZFTI03 = TOTALZFTI03 + weightsZ["FTI03"]
            TOTALZFTI04 = TOTALZFTI04 + weightsZ["FTI04"]
            TOTALZFTI05 = TOTALZFTI05 + weightsZ["FTI05"]
            TOTALZFTI06 = TOTALZFTI06 + weightsZ["FTI06"]
            TOTALZFTI07 = TOTALZFTI07 + weightsZ["FTI07"]
            TOTALZFTI08 = TOTALZFTI08 + weightsZ["FTI08"]
            TOTALZFTI09 = TOTALZFTI09 + weightsZ["FTI09"]
            
            #Total_zjc = Total_zjc + weightsZ["JC"]
            
    WAA = []
    WAA.append((1 / (numpy.log10(TOTALZFTI01)   + 0.00001)) * WCN[0])
    WAA.append((1 / (numpy.log10(TOTALZFTI02)   + 0.00001)) * WCN[1])
    WAA.append((1 / (numpy.log10(TOTALZFTI03)   + 0.00001)) * WCN[2])
    WAA.append((1 / (numpy.log10(TOTALZFTI04)   + 0.00001)) * WCN[3])
    WAA.append((1 / (numpy.log10(TOTALZFTI05)   + 0.00001)) * WCN[4])
    WAA.append((1 / (numpy.log10(TOTALZFTI06)   + 0.00001)) * WCN[5])
    WAA.append((1 / (numpy.log10(TOTALZFTI07)   + 0.00001)) * WCN[6])
    WAA.append((1 / (numpy.log10(TOTALZFTI08)   + 0.00001)) * WCN[7])
    WAA.append((1 / (numpy.log10(TOTALZFTI09)   + 0.00001)) * WCN[8])
    
    
    return {'WCN': WCN, 'WAA': WAA }
    
    
    

def generateWeights(graph, weightFile, param):
    pdb = Base(weightFile)
    pdb.create('pair', 'node1', 'node2','FTI01','FTI02','FTI03','FTI04','FTI05','FTI06','FTI07','FTI08','FTI09')
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
                FTI01 = total_publications * (0.1**k)
                FTI02 = total_publications * (0.2**k)
                FTI03 = total_publications * (0.3**k)
                FTI04 = total_publications * (0.4**k)
                FTI05 = total_publications * (0.5**k)
                FTI06 = total_publications * (0.6**k)
                FTI07 = total_publications * (0.7**k)
                FTI08 = total_publications * (0.8**k)
                FTI09 = total_publications * (0.9**k)
                 
                
 
                pdb.insert(str(node) + ';' + str(other),node,other, FTI01, FTI02, FTI03, FTI04, FTI05, FTI06, FTI07, FTI08, FTI09 ) 
                 
    pdb.commit()            
    return pdb

def calculatingWeights(graph, nodesnotLinked, database, calculatingFile):
    pdb = Base(calculatingFile)
    pdb.create('node1', 'node2', 'WCNFTI01','WCNFTI02', 'WCNFTI03','WCNFTI04','WCNFTI05','WCNFTI06','WCNFTI07','WCNFTI08','WCNFTI09','WAAFTI01','WAAFTI02', 'WAAFTI03','WAAFTI04','WAAFTI05','WAAFTI06','WAAFTI07','WAAFTI08','WAAFTI09')
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
        WCNFTI01 = 0;
        WCNFTI02 = 0;
        WCNFTI03 = 0;
        WCNFTI04 = 0;
        WCNFTI05 = 0;
        WCNFTI06 = 0;
        WCNFTI07 = 0;
        WCNFTI08 = 0;
        WCNFTI09 = 0;
        
        WAAFTI01 = 0;
        WAAFTI02 = 0;
        WAAFTI03 = 0;
        WAAFTI04 = 0;
        WAAFTI05 = 0;
        WAAFTI06 = 0;
        WAAFTI07 = 0;
        WAAFTI08 = 0;
        WAAFTI09 = 0;
        
        
        for cn in CommonNeigbors:
            item = get_partOfWeightCalculating(graph, database, pair, cn)
            WCNFTI01 = WCNFTI01 + item['WCN'][0];
            WCNFTI02 = WCNFTI02 + item['WCN'][1];
            WCNFTI03 = WCNFTI03 + item['WCN'][2];
            WCNFTI04 = WCNFTI04 + item['WCN'][3];
            WCNFTI05 = WCNFTI05 + item['WCN'][4];
            WCNFTI06 = WCNFTI06 + item['WCN'][5];
            WCNFTI07 = WCNFTI07 + item['WCN'][6];
            WCNFTI08 = WCNFTI08 + item['WCN'][7];
            WCNFTI09 = WCNFTI09 + item['WCN'][8];
            
            WAAFTI01 = WAAFTI01 + item['WAA'][0];
            WAAFTI02 = WAAFTI02 + item['WAA'][1];
            WAAFTI03 = WAAFTI03 + item['WAA'][2];
            WAAFTI04 = WAAFTI04 + item['WAA'][3];
            WAAFTI05 = WAAFTI05 + item['WAA'][4];
            WAAFTI06 = WAAFTI06 + item['WAA'][5];
            WAAFTI07 = WAAFTI07 + item['WAA'][6];
            WAAFTI08 = WAAFTI08 + item['WAA'][7];
            WAAFTI09 = WAAFTI09 + item['WAA'][8];
            
        pdb.insert(str(pair[0]), str(pair[1]), WCNFTI01, WCNFTI02,  WCNFTI02,
                   WCNFTI03,WCNFTI04,WCNFTI05,WCNFTI06,WCNFTI07,WCNFTI08,WCNFTI09,
                   WAAFTI01, WAAFTI02,  WAAFTI02,
                   WAAFTI03,WAAFTI04,WAAFTI05,WAAFTI06,WAAFTI07,WAAFTI08,WAAFTI09,
                    
                    )   
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

def analise(calcDb, topRank,TestGraph, util, method):
    order = sorted( list({ 'node1': r['node1'], 'node2': r['node2'], 'value' : r[method]} for r in calcDb)  , key=lambda value: value['value'], reverse=True)
    BD = None
    if not os.path.exists(FormatingDataSets.get_abs_file_path(util.calculated_file + '.' + method +'.base.pdl')):
        BD = generate_finalResult(order, topRank, TestGraph, FormatingDataSets.get_abs_file_path(util.calculated_file + '.' + method +'.base.pdl'))
    
    else:
        BD = reading_Database(FormatingDataSets.get_abs_file_path(util.calculated_file + '.' + method +'.base.pdl'))
    
    return get_results(BD, method)
    

def get_analyseNodesInFuture(calcDb, topRank, TestGraph, util):
    
    result = []
    
    result.append(analise(calcDb, topRank, TestGraph, util, 'WCNFTI01'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WCNFTI02'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WCNFTI03'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WCNFTI04'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WCNFTI05'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WCNFTI06'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WCNFTI07'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WCNFTI08'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WCNFTI09'))
    
    result.append(analise(calcDb, topRank, TestGraph, util, 'WAAFTI01'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WAAFTI02'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WAAFTI03'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WAAFTI04'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WAAFTI05'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WAAFTI06'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WAAFTI07'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WAAFTI08'))
    result.append(analise(calcDb, topRank, TestGraph, util, 'WAAFTI09'))
    
    
    
    
    
    return result    
    

def reading_Database(path):
    adb = Base(path)
    adb.open()
    return adb



    

def execution(configFile):
   
    
    #DEFINE THE FILE THAT WILL KEEP THE RESULT DATA
    resultFile = open(FormatingDataSets.get_abs_file_path(configFile + 'FTI.txt'), 'w')
    
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
    grqc()
    astroph()
    hepth()
    hepph()
    condmat()
    grqc05()
    astroph05()
    hepth05()
    hepph05()
    condmat05()
    #astroph()
    #hepth()
    #hepph()
    #condmat()
    #grqc05()
    #astroph05()
    #hepth05()
    #hepph05()
    #condmat05()
    #mas99()
    #mas05()
    
    