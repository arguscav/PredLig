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
from calculating.CalculatingTogether import CalculatingTogether


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
    #CREATING CALCULATION OBJECT
    calc = CalculatingTogether(myparams, nodeSelection.nodesNotLinked)
    
    ordering = calc.ordering(len(nodeSelection.eNeW))
    
    calc.AnalyseNodesInFuture(ordering, myparams.testGraph)
    
    resultFile.write(repr(calc.get_TotalSucess()))
    
    resultFile.write("\n")
#        
    resultFile.write("Authors\tArticles\tCollaborations\tAuthors\tEold\tEnew\n")
    resultFile.write( str(myparams.get_nodes(myparams.trainnigGraph))+ "\t" + str(myparams.get_edges(myparams.trainnigGraph)) + "\t\t" + str(len(nodeSelection.get_NowellColaboration())*2)+ "\t\t" + str(len(nodeSelection.nodes)) + "\t" + str(len(nodeSelection.eOld))+"\t" + str(len(nodeSelection.eNeW)))
     
 
    resultFile.write("\n")

    resultFile.write("Fim da Operacao\n")
    resultFile.write(str(datetime.datetime.now()))
    
    resultFile.close()

def grqc():
    configFile = 'data/configuration/arxiv/grqc/MetricaTemporal/config_NOWELLTSRich.txt'
    execution(configFile)

def astroph():
    configFile = 'data/configuration/arxiv/astroph/MetricaTemporal/config_NOWELLTSRich.txt'
    execution(configFile)

def condmat():
    configFile = 'data/configuration/arxiv/condmat/MetricaTemporal/config_NOWELLTSRich.txt'
    execution(configFile)
    
def hepth():
    configFile = 'data/configuration/arxiv/hepth/MetricaTemporal/config_NOWELLTSRich.txt'
    execution(configFile)

def hepph():
    configFile = 'data/configuration/arxiv/hepph/MetricaTemporal/config_NOWELLTSRich.txt'
    execution(configFile)

if __name__ == '__main__':
    grqc()
    astroph()
    hepth()
    hepph()
    condmat()
    
    