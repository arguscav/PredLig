'''
Created on Dec 19, 2015

@author: cptullio
'''
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from datetime import datetime
from calculating.NodeSelection import NodeSelection
from calculating.CalculatingCombinationTogetherOnlyNowell import CalculatingCombinationOnlyNowell
from formating.FormatingDataSets import FormatingDataSets


def execution(configFile, weights):
    #DEFINE THE FILE THAT WILL KEEP THE RESULT DATA
    resultFile = open(FormatingDataSets.get_abs_file_path(configFile + 'core03.txt'), 'w')
    
    resultFile.write("Inicio da operacao\n")
    resultFile.write(str(datetime.now()))
    resultFile.write("\n")
    #READING THE CONFIG FILE
    util = ParameterUtil(parameter_file = configFile)
    
    myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, linear_combination=util.linear_combination,
                                filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None, result_random_file=util.result_random_file)
    
    myparams.generating_Test_Graph()
    myparams.generating_Training_Graph()
    
    nodeSelection = NodeSelection(myparams.trainnigGraph, myparams.testGraph, util)
    #CREATING CALCULATION OBJECT
    calc = CalculatingCombinationOnlyNowell(myparams, nodeSelection.nodesNotLinked, weights, True)
        
    ordering = calc.ordering(len(nodeSelection.eNeW))
    
    calc.AnalyseNodesInFuture(ordering, myparams.testGraph)
    
    resultFile.write(repr(calc.get_TotalSucess()))
    
    resultFile.write("\n")
#        
    resultFile.write("Authors\tArticles\tCollaborations\tAuthors\tEold\tEnew\n")
    resultFile.write( str(myparams.get_nodes(myparams.trainnigGraph))+ "\t" + str(myparams.get_edges(myparams.trainnigGraph)) + "\t\t" + str(len(nodeSelection.get_NowellColaboration())*2)+ "\t\t" + str(len(nodeSelection.nodes)) + "\t" + str(len(nodeSelection.eOld))+"\t" + str(len(nodeSelection.eNeW)))
     
 
    resultFile.write("\n")

    resultFile.write("Fim da Operacao\n")
    resultFile.write(str(datetime.now()))
    
    resultFile.close()
    
def grqc():
    configFile = 'data/configuration/arxiv/grqc/CombinationLinear/config_NOWELLTS_FROMAG.txt'
    
    #execution(configFile, ['cn', 'aas', 'ts05'])

    weights = {'cn' : 0.300955064105, 'aas': 0.783119689943, 'pa':0, 'jc': 0, 'ts08':0,'ts05': 0.298981048518, 'ts02':0}
    
    execution(configFile, weights)
    
def hepth():
    configFile = 'data/configuration/arxiv/hepth/CombinationLinear/config_NOWELLTS_FROMAG.txt'
    
    #execution(configFile, ['jc', 'aas', 'ts02'])

    weights = {'cn' : 0, 'aas': 0.783119689943, 'pa':0, 'jc': 0.300955064105, 'ts08':0,'ts05': 0, 'ts02':0.298981048518}
    
    execution(configFile, weights)

    
def hepph():
    configFile = 'data/configuration/arxiv/hepph/CombinationLinear/config_NOWELLTS_FROMAG.txt'
    
    #execution(configFile, ['jc', 'aas', 'ts02'])

    weights = {'cn' : 0, 'aas': 0.624674557702, 'pa':0, 'jc': -0.12279209072, 'ts08':0,'ts05': 0, 'ts02':0.234818778333}
    
    execution(configFile, weights)
        
def condmat():
    configFile = 'data/configuration/arxiv/condmat/CombinationLinear/config_NOWELLTS_FROMAG.txt'
    
    #execution(configFile, ['jc', 'aas', 'ts02'])

    weights = {'cn' : 0, 'aas': 0.912812143425, 'pa':0, 'jc': 5.52219292056, 'ts08':0,'ts05': 0, 'ts02':2.27572876652}
    
    execution(configFile, weights)


def astroph():
    configFile = 'data/configuration/arxiv/astroph/CombinationLinear/config_NOWELLTS_FROMAG.txt'
    
  #execution(configFile, ['cn', 'aas', 'ts02'])

    weights = {'cn' : -0.510981548519, 'aas': 0.608979986963, 'pa':0, 'jc': 0, 'ts08':0,'ts05': 0, 'ts02':0.359358925465}
    
    execution(configFile, weights)



if __name__ == '__main__':
    grqc()
    hepph()
    hepth()
    astroph()
    condmat()