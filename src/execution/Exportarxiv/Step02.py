'''
Created on Aug 22, 2015

@author: cptullio
Process of partition the graph in two for training and for test

'''
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
import networkx
import matplotlib

import hashlib
if __name__ == '__main__':
    #util = ParameterUtil(parameter_file = 'data/formatado/arxiv/pankaj_condmat_2004_2012/config/configurationG1.txt')
    util = ParameterUtil(parameter_file = 'data/formatado/arxiv/exemplomenor/config/config.txt')
    
    #util = ParameterUtil(parameter_file = 'data/formatado/arxiv/nowell_astroph_1994_1999/AllExecutionScores/config.txt')
    
    myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, linear_combination=util.linear_combination,
                                filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None, result_random_file=util.result_random_file)

    
    # Assumes the default UTF-8
    #print hashlib.binascii(hashlib.sha1(mystring))
    #hash_object = hashlib.md5(mystring.encode()).hexdigest()
    #print(hash_object.hexdigest())
    #hex_dig = hash_object.hexdigest()
    #print(hex_dig)

    #graph_path = '/Users/cptullio/git/Predicao-de-Links/PredLig/src/formating/data/formatado/arxiv/astroph_graph_1994_1999.txt'
    #graph = networkx.read_graphml(graph_path)
    #papers = set(aresta['id_edge'] for no1,no2,aresta in graph.edges(data=True) if  1==1)
    
    #print 'TOTAL DE PAPERS:', len(papers)
    #print 'TOTAL DE AUTORES:', len(graph.nodes())
    #allPapers = graph.edges(data=True)
    #print allPapers[0]
    
    #arestas = list([no1,no2,aresta] for no1,no2,aresta in graph.edges(data=True) if  aresta['time'] >= 1996 and aresta['time'] <= 1997)
    #print arestas[0]
    #papers[0]    
    #networkx.draw_networkx(graph)
    #matplotlib.pyplot.show()
    myparams.generating_Training_Graph()
    myparams.generating_Test_Graph()
    
    