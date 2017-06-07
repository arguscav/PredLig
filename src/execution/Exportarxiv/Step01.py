'''
Created on Aug 22, 2015

@author: cptullio

First Step is the generation of the graph from the database informations.
We will need the file of parameter to indicate the place where the graph will be saved

'''
from parametering.ParameterUtil import ParameterUtil

from formating.arxiv.Formating import Formating

if __name__ == '__main__':
    util = ParameterUtil(parameter_file = 'data/configuration/arxiv/exemplo_1994_1999/CombinationLinear/configToAG.txt')
    #util = ParameterUtil(parameter_file = 'data/configuration/arxiv/condmat_1994_1999/MetricaTemporal/config.txt')
    
    #myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, 
    #                        filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None)

    
    astroPh = Formating(util.graph_file)
    astroPh.subject = 'cond-mat'
    #astroPh.yearstoRescue = [1993]
    astroPh.yearstoRescue = [1994,1995,1996,1997,1998,1999]
    #astroPh.yearstoRescue = [2004,2005,2006,2007,2008,2009, 2010, 2011, 2012]
    #astroPh.readingOrginalDataset()
    astroPh.generating_graph()
    astroPh.saveGraph()