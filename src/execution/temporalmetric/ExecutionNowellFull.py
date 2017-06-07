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


def execution(configFile):
    #DEFINE THE FILE THAT WILL KEEP THE RESULT DATA
    resultFile = open(FormatingDataSets.get_abs_file_path(configFile + 'T.EXPERIMENTO_ATUAL_CORE03.txt'), 'w')
    
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
    nodesSelection = NodeSelection(myparams.trainnigGraph, myparams.testGraph, util)
    #GET THE AUTHORS THAT PUBLISH AT TRAINNING AND TEST 
    #A NUMBER OF PAPERS DEFINED AT MIN_EDGES IN CONFIG FILE
    nodes = nodesSelection.get_NowellAuthorsCore()
    #GET A PAIR OF AUTHORS THAT PUBLISH AT LEAST ONE ARTICLE AT TRAINNING AND TEST.
    #DID NOT SEE ANY NEED
    collaborations = nodesSelection.get_NowellColaboration()
    #GET THE FIRST EDGES MADE BY THE COMBINATION OF NODES IN TRAINNING GRAPH
    eOld = nodesSelection.get_NowellE(nodes,myparams.trainnigGraph)
    #GET THE FIRST EDGES MADE BY THE COMBINATION OF NODES IN TEST GRAPH THAT DO NOT HAVE EDGES IN TRAINNING
    eNew = nodesSelection.get_NowellE2(nodes, eOld, myparams.testGraph)
    #GET THE NODES NOT LINKED OVER THE COMBINATION NODES.
    nodesNotLinked = nodesSelection.get_PairsofNodesNotinEold(nodes)
    #CREATING CALCULATION OBJECT
    calc = CalculateInMemory(myparams,nodesNotLinked)
    #CALCULATING THE SCORES.
    resultsofCalculation = calc.executingCalculate()
    #ORDERNING THE RESULTS RETURNING THE TOP N 
    orderingResults = calc.ordering(len(eNew), resultsofCalculation)
    #SAVING THE ORDERED RESULTS.
    calc.saving_orderedResult(util.ordered_file, orderingResults)
    #ANALISE THE ORDERED RESULTS AND CHECK THE FUTURE.
    ScoresResults = Analyse.AnalyseNodesWithScoresInFuture(orderingResults, myparams.testGraph)
    #SAVING THE RESULTS.  
    for index in range(len(ScoresResults)):
        Analyse.saving_analyseResult(ScoresResults[index], util.analysed_file + str(myparams.ScoresChoiced[index][0] ) + '.txt')
        resultFile.write("TOTAL OF SUCESSS USING METRIC "  + str(myparams.ScoresChoiced[index][0])  + " = " +  str(Analyse.get_TotalSucess(ScoresResults[index]) ))
        resultFile.write("\n")
        resultFile.write("\n")
         
    resultFile.write("Authors\tArticles\tCollaborations\tAuthors\tEold\tEnew\n")
    resultFile.write( str(myparams.get_nodes(myparams.trainnigGraph))+ "\t" + str(myparams.get_edges(myparams.trainnigGraph)) + "\t\t" + str(len(collaborations)*2)+ "\t\t" + str(len(nodes)) + "\t" + str(len(eOld))+"\t" + str(len(eNew)))
     
    resultFile.write("\n")

    resultFile.write("Fim da Operacao\n")
    resultFile.write(str(datetime.datetime.now()))
    
    resultFile.close()

def astroph():
    configFile = 'data/configuration/arxiv/astroph_2010_2015/MetricaTemporal/config.txt'
    execution(configFile)


def astrophTS05():
    configFile = 'data/configuration/arxiv/astroph_2010_2015/MetricaTemporal/config05.txt'
    execution(configFile)

def astrophTS02():
    configFile = 'data/configuration/arxiv/astroph_2010_2015/MetricaTemporal/config02.txt'
    execution(configFile)

def condmat():
    configFile = 'data/configuration/arxiv/condmat_2010_2015/MetricaTemporal/config.txt'
    execution(configFile)
    
def condmatTS05():
    configFile = 'data/configuration/arxiv/condmat_2010_2015/MetricaTemporal/config05.txt'
    execution(configFile)

def condmatTS02():
    configFile = 'data/configuration/arxiv/condmat_2010_2015/MetricaTemporal/config02.txt'
    execution(configFile)

def grqc():
    configFile = 'data/configuration/arxiv/grqc_1994_1999/MetricaTemporal/config.txt'
    execution(configFile)

    
def grqcTS02():
    configFile = 'data/configuration/arxiv/grqc_2010_2015/MetricaTemporal/config02.txt'
    execution(configFile)

def grqcTS05():
    configFile = 'data/configuration/arxiv/grqc_2010_2015/MetricaTemporal/config05.txt'
    execution(configFile)


def hepth():
    configFile = 'data/configuration/arxiv/hepth_2010_2015/MetricaTemporal/config.txt'
    execution(configFile)
        
def hepthTS05():
    configFile = 'data/configuration/arxiv/hepth_2010_2015/MetricaTemporal/config05.txt'
    execution(configFile)

def hepthTS02():
    configFile = 'data/configuration/arxiv/hepth_2010_2015/MetricaTemporal/config02.txt'
    execution(configFile)

def hepph():
    configFile = 'data/configuration/arxiv/hepph_2010_2015/MetricaTemporal/config.txt'
    execution(configFile)


def hepphTS02():
    configFile = 'data/configuration/arxiv/hepph_2010_2015/MetricaTemporal/config02.txt'
    execution(configFile)

    
def hepphTS05():
    configFile = 'data/configuration/arxiv/hepph_2010_2015/MetricaTemporal/config05.txt'
    execution(configFile)


def mas():
    configFile = 'data/configuration/arxiv/MAS_1994_1999/MetricaTemporal/config.txt'
    execution(configFile)


def mas02():
    configFile = 'data/configuration/arxiv/MAS_1994_1999/MetricaTemporal/config2.txt'
    execution(configFile)

    
def mas05():
    configFile = 'data/configuration/arxiv/MAS_1994_1999/MetricaTemporal/config5.txt'
    execution(configFile)

    
    
if __name__ == '__main__':
    #mas()
    #mas02()
    #mas05()
    grqc()
    