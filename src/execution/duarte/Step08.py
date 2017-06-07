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
    util = ParameterUtil(parameter_file = 'data/formatado/duarte/nowell_duarte_1994_1999.txt')
    myparams = Parameterization(util.keyword_decay, util.lengthVertex, util.t0, util.t0_, util.t1, util.t1_, util.FeaturesChoiced, util.graph_file, util.trainnig_graph_file, util.test_graph_file, util.decay)
    myparams.generating_Training_Graph()
    myparams.generating_Test_Graph()
    print "Trainning Period:", myparams.t0, " - ", myparams.t0_
    print "Test Period:", myparams.t1, " - ", myparams.t1_
    
    print "# Papers in Trainning: ",  myparams.get_edges(myparams.trainnigGraph)
    print "# Authors in Training: ", myparams.get_nodes(myparams.trainnigGraph)
    print "# Papers in Test: ",  myparams.get_edges(myparams.testGraph)
    print "# Authors in Test", myparams.get_nodes(myparams.testGraph)
    