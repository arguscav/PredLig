'''
Created on 12 de jun de 2016

@author: Administrador
'''
import gc
from formating.arxiv.Formating import Formating
import os
from datetime import datetime

class NodeSelection(object):


    def AnalyseAllNodesNotLinkedInFuture(self, nodesNotLinked, TestGraph):
        result = []
        for pair in nodesNotLinked:
            if (TestGraph.has_edge(pair[0],pair[1])):
                result.append([pair[0],pair[1],1])
            else:
                result.append([pair[0],pair[1],0])
        return result

    def get_PairsofNodesNotinEold(self,  nodes):
        pares = []
        total= 0
        for pair in sorted(nodes):
            others = set(n for n in nodes if n > pair)
            for other in others:
                if not self.trainnigGraph.has_edge(pair, other):
                    pares.append([pair,other])
                    total = total + 1
                  
        print total
        return pares
    
    def get_NowellE(self, CoreAuthors, graph):
        result = []
        for node in sorted(CoreAuthors):
            othernodes = set(n for n in CoreAuthors if n > node)
            for other in othernodes:
                if graph.has_edge(node, other):
                    result.append({node, other})
        return result
    
    def existInTranning(self, node, other, trainningData):
        for data in trainningData:
            v = list(data)
            if (node == v[0] and other == v[1]) or (node == v[1] and other == v[0]):
                return True
        return False
    
    
    def get_NowellE2(self, CoreAuthors, trainningData, graph):
        result = []
        for node in sorted(CoreAuthors):
            othernodes = set(n for n in CoreAuthors if n > node)
            for other in othernodes:
                if graph.has_edge(node, other):
                    if not self.existInTranning(node, other, trainningData):
                        result.append({node, other})
                    
        return result
    

    def get_NowellColaboration(self):
        result = []
        mynodestranningGraph = sorted(set(self.trainnigGraph.nodes()))
        for node in mynodestranningGraph:
            othernodes = set(n for n in mynodestranningGraph if n > node)
            for other in othernodes:
                if self.trainnigGraph.has_edge(node, other):
                    result.append({node, other})
                    
        return result
    

    def get_NowellAuthorsCore(self):
        mynodestestGraph = set(self.testGraph.nodes())
        mynodestranningGraph = set(self.trainnigGraph.nodes())
        total = mynodestestGraph.intersection(mynodestranningGraph)
        
        result = set()
        for node in total:
            test = set(aresta['id_edge'] for no1,no2,aresta in self.testGraph.edges(node, data=True) if  1==1)
            train = set(aresta['id_edge'] for no1,no2,aresta in self.trainnigGraph.edges(node, data=True) if  1==1)
            
            if len(test) >= self.util.min_edges and len(train) >=self.util.min_edges:
                result.add(node)
        
        
        del mynodestestGraph
        del mynodestranningGraph
        del total
        total = None
        mynodestestGraph = None
        mynodestranningGraph = None
        gc.collect()
        return result
    
    def saveResults(self, filepath, nodesNotLinked):
        myfile = Formating.get_abs_file_path(filepath)
        with open(myfile, 'w') as fileNodesNotLinked:
            for nodeNotLinked in nodesNotLinked:
                fileNodesNotLinked.write(nodeNotLinked[0] + ',' +  nodeNotLinked[1] + '\n')
            fileNodesNotLinked.close()
    
    def readingResultsFile(self, filepath):
        results = []
        myfile = Formating.get_abs_file_path(filepath)
        with open(myfile, 'r') as fileNodesNotLinked:
            for lineofFile in fileNodesNotLinked:
                nodenotllinked = lineofFile.replace('\n', '').split(',')
                results.append([nodenotllinked[0],nodenotllinked[1]])
            fileNodesNotLinked.close()
        return results
    
    

    def __init__(self, trainnigGraph, testGraph, paramsUtil):
        
        self.trainnigGraph = trainnigGraph
        self.testGraph = testGraph
        self.util = paramsUtil
        print "selecting node informations", datetime.now()
        self.nodes = self.get_NowellAuthorsCore()
        self.eOld = self.get_NowellE(self.nodes, self.trainnigGraph)
        self.eNeW = self.get_NowellE2(self.nodes, self.eOld, self.testGraph)
        print "generating nodes not linked", datetime.now()
        self.nodesNotLinked = self.get_PairsofNodesNotinEold(self.nodes)
        
        
        
        