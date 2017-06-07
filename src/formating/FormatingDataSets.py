'''
Created on Jun 14, 2015

@author: cptullio
'''
from abc import abstractmethod
from os import path
import os
import networkx
from datetime import datetime

class FormatingDataSets(object):
    
    @staticmethod
    def getTotalLineNumbers(filepath):
        linenumber = 0
        with open(filepath,'r') as f:
            for line in f:
                linenumber = linenumber + 1
            f.close()
        return linenumber
        
    
    @staticmethod
    def get_abs_file_path(relativepath):
        script_path = path.abspath(__file__) 
        script_dir = path.split(script_path)[0]
        pathFinal = path.join(script_dir, relativepath)
    
        dir = path.dirname(pathFinal)
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        return pathFinal
    
    @staticmethod
    def printProgressofEvents(element, length, message):
        print message, str((float(element)/float(length))*float(100)) + '%', datetime.today()
    
    
    @staticmethod
    def reading_graph(relativepath):
        abs_path = FormatingDataSets.get_abs_file_path(relativepath)
        return networkx.read_graphml(abs_path, unicode)
    
    def saveGraph(self):
        networkx.write_graphml(self.Graph, self.get_abs_file_path(self.GraphFile)) 
    
    
    @staticmethod
    def get_graph_from_period(graph, t0,t0_):
        print "Starting generating graph from period", datetime.today()
        arestas = list([no1,no2,aresta] for no1,no2,aresta in graph.edges(data=True) if  aresta['time'] >= t0 and aresta['time'] <= t0_)
        new_graph = networkx.MultiGraph()
        new_graph.add_edges_from(arestas)
        
        print "Generating graph from period finished", datetime.today()
        
        return new_graph    
    
    @staticmethod
    def reading_file(abs_file):
        content = None
        with open(abs_file) as f:
            content = f.readlines()
            f.close()
        return content


    @abstractmethod      
    def readingOrginalDataset(self):
        raise RuntimeError('not implemented')
    
    
    def __init__(self, filePathOriginalDataSet, graphfile):
        self.Graph = None
        self.GraphFile = graphfile
        self.OriginalDataSet = self.get_abs_file_path(filePathOriginalDataSet)
        
        