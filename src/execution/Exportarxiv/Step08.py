'''
Created on 28 de ago de 2015

@author: CarlosPM
For statistics results

'''
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from formating.FormatingDataSets import FormatingDataSets
from analysing.Analyse import Analyse
from calculating.Calculate import Calculate

if __name__ == '__main__':
   
    util = ParameterUtil(parameter_file = 'data/formatado/arxiv/exemplomenor/config/configuration_weights.txt')
    myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, 
                                filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None)

 
   
    myparams.generating_Training_Graph()
    myparams.generating_Test_Graph()
    print "Trainning Period:", myparams.t0, " - ", myparams.t0_
    print "Test Period:", myparams.t1, " - ", myparams.t1_
    
    print "# Papers in Trainning: ",  myparams.get_edges(myparams.trainnigGraph)
    print "# Authors in Training: ", myparams.get_nodes(myparams.trainnigGraph)
    print "# Papers in Test: ",  myparams.get_edges(myparams.testGraph)
    print "# Authors in Test", myparams.get_nodes(myparams.testGraph)
    
    calc = Calculate(myparams, util.nodes_notlinked_file, util.calculated_file, util.ordered_file, util.maxmincalculated_file)
    calc.reading_Max_min_file()
    print "# pair of Authors with at least 3 articles Calculated: ", calc.qtyDataCalculated  #FormatingDataSets.getTotalLineNumbers(FormatingDataSets.get_abs_file_path(util.calculated_file))
    topRank = Analyse.getTopRank(util.analysed_file+ '.random.analised.txt')
    print "# pair of Authors with at least 3 articles that is connected in Test Graph in a random way: ", topRank
    print "Max values found in calculations: ", str(calc.maxValueCalculated)
    print "Min Values found in calculations: ", str(calc.minValueCalculated)
    for pathFile in calc.getfilePathOrdered_separeted():
        print "File Analised: ", pathFile +  '.analised.txt'
        number_connected =  Analyse.getTopRankABSPathFiles(pathFile + '.analised.txt')
        print "# pair of Authors that is connected in Test Graph: ", number_connected
        print "%: ", Analyse.getLastInfosofResultsABSPathFiles(pathFile + '.analised.txt', topRank)
        print "---------------------------------"