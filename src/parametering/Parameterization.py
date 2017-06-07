'''
Created on Jun 15, 2015

@author: cptullio
'''
import networkx
from formating.dblp.Formating import Formating
import os.path
from datetime import datetime
import gc
from pydblite import Base


class Parameterization(object):
    
    def generating_Test_Graph(self ):
        if not os.path.exists(Formating.get_abs_file_path(self.filePathTestGraph)):
            if self.graph == None:
                print "Reading Full graphs", datetime.today()
                self.graph = Formating.reading_graph(self.filePathGraph)
            print "Generating Testing graphs", datetime.today()
        
            self.testGraph = Formating.get_graph_from_period(self.graph, self.t1, self.t1_)
            networkx.write_graphml(self.testGraph, Formating.get_abs_file_path(self.filePathTestGraph))
        else:
            print "Reading testing graph", datetime.today()
            self.testGraph = Formating.reading_graph(self.filePathTestGraph)
            
    def generating_Training_Graph(self):
        if not os.path.exists(Formating.get_abs_file_path(self.filePathTrainingGraph)):
            if self.graph == None:
                print "Reading Full graphs", datetime.today()
                self.graph = Formating.reading_graph(self.filePathGraph)
            
            print "Generating Trainnig graphs", datetime.today()
           
            self.trainnigGraph = Formating.get_graph_from_period(self.graph, self.t0, self.t0_)
            
            networkx.write_graphml(self.trainnigGraph, Formating.get_abs_file_path(self.filePathTrainingGraph))
        else:
            print "Reading Trainnig graph", datetime.today()
            self.trainnigGraph = Formating.reading_graph(self.filePathTrainingGraph)
        
        for w_score in self.WeightedScoresChoiced:
            w_score[0].graph = self.trainnigGraph
        for score in self.ScoresChoiced:
            score[0].graph = self.trainnigGraph
        for w in self.WeightsChoiced:
            w[0].graph = self.trainnigGraph 
    
    def get_edges(self, graph):
        myedges = set(aresta['id_edge'] for no1,no2,aresta in graph.edges(data=True) if  1==1)
        result = len(myedges)
        myedges = None
        gc.collect()
        return result
    
    def get_new_edges(self, tranningGraph, testGraph):
        myedgestestGraph = set(aresta['id_edge'] for no1,no2,aresta in testGraph.edges(data=True) if  1==1)
        myedgestranningGraph = set(aresta['id_edge'] for no1,no2,aresta in tranningGraph.edges(data=True) if  1==1)
        diference = myedgestestGraph.difference(myedgestranningGraph)
        newEdges = 0
        for edge in diference:
            pair = list(list({no1,no2} for no1,no2,aresta in 
                             testGraph.edges(data=True) if aresta['id_edge'] == edge)[0])
            #print pair
            if len(pair) == 1:
                if not tranningGraph.has_node(pair[0]):
                    if len(testGraph.edges(pair[0])) >= 3:
                        newEdges = newEdges + 1
            else:
                if len(tranningGraph.edges(pair[0])) >= 3 and len(tranningGraph.edges(pair[1])) >= 3 and len(testGraph.edges(pair[0])) >= 3 and  len(testGraph.edges(pair[1])) >= 3:
                    if tranningGraph.has_node(pair[0]) and tranningGraph.has_node(pair[1]):
                        if not tranningGraph.has_edge(pair[0], pair[1]):
                            newEdges = newEdges + 1
                    else:
                        newEdges = newEdges + 1
            
            
        myedgestestGraph = None
        myedgestranningGraph = None
        gc.collect()
        return newEdges
    
    
    
    
        
    
    
    
    def get_nodes(self, graph):
        mynodes = graph.nodes()
        result =  len(mynodes)
        del mynodes
        mynodes = None
        gc.collect()
        return result
    
    def get_nodesWithPaperControl(self, graph):
        mynodes = graph.nodes()
        total = 0
        for node in mynodes:
            qtde = len(graph.edges(node))
            if qtde >= self.min_edges:
                total = total + 1
        #result =  len(mynodes)
        del mynodes
        mynodes = None
        gc.collect()
        return total
    
    
    def getQtyofEdges(self,graph):
        if self.qtyofEdges == None:
            self.qtyofEdges =  self.get_edges(graph)
        return self.qtyofEdges
      
    def generateDataForCalculate(self):
        if self.trainnigGraph == None:
            self.generating_Training_Graph()
        
        _nodes = sorted(self.trainnigGraph.nodes())
        adb = Base(self.filePathTrainingGraph + ".calc.pdl")
        adb.create('pairNodes', 'common', 'time', 'domain' )
        
        for node in sorted(_nodes):
            othernodes = set(n for n in _nodes if n > node)
            for other in othernodes:
                common =  set(networkx.common_neighbors(self.trainnigGraph, node, other))
                arestas = self.trainnigGraph.edges([node, other], True)
                     
        
        
   
    
    def __init__(self, 
                 t0, t0_, t1, t1_, 
                 filePathGraph, 
                 filePathTrainingGraph, 
                 filePathTestGraph, 
                 linear_combination,
                 decay,
                 domain_decay, 
                 min_edges = 1, 
                 scoreChoiced = None, 
                 weightsChoiced = None, 
                 weightedScoresChoiced = None,
                 FullGraph = None, result_random_file = None):
        
        self.qtyofEdges = None
        self.ScoresChoiced = scoreChoiced
        self.WeightsChoiced = weightsChoiced
        self.WeightedScoresChoiced = weightedScoresChoiced
        self.min_edges = min_edges
        self.domain_decay = domain_decay
        self.linear_combination = linear_combination
        self.decay = decay
        self.t0_ = t0_
        self.t0 = t0
        self.t1 = t1
        self.t1_ = t1_
        self.graph = FullGraph
        self.filePathGraph = filePathGraph
        self.filePathTrainingGraph = filePathTrainingGraph
        self.filePathTestGraph = filePathTestGraph
        self.linkObjects = {}
        self.nodeObjects = {}
        self.result_random_file = result_random_file
        self.debugar = False
     
        
       
         
        