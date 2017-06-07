'''
Created on Jul 1, 2015

@author: cptullio
'''
import networkx
import os.path
from formating.dblp.Formating import Formating
from datetime import datetime
from formating.FormatingDataSets import FormatingDataSets


class VariableSelection(object):

    @staticmethod
    def getItemFromLine(lineofFile):
        cols = lineofFile.strip().replace('\n','').split(',')
        return [cols[0], cols[1]]
    
    
    def get_all_pair_nodes(self, graph):
        result = []
        nodesinGraph =self.graph.nodes()
        nodesOrdered = sorted(nodesinGraph)
        
        for node1 in nodesOrdered:
            others =  set(n for n in nodesOrdered if n > node1)
            for otherNode in others:
                result.append([node1,otherNode])
        return result
            
        
  
    def get_pair_nodes_not_linked(self):
        print "Starting getting pair of nodes that is not liked", datetime.today()
        results = []
        nodesinGraph =self.graph.nodes()
        nodesOrdered = sorted(nodesinGraph)
        totalnodesOrdered = len(nodesOrdered)
        element = 0
        
        for node in nodesOrdered:
            element = element+1
            FormatingDataSets.printProgressofEvents(element, totalnodesOrdered, "Checking Node not liked: ")
            publicacoes = self.graph.edges(node,data=False)
            qtdepublicacoes = len(publicacoes)
            #print "O autor e seus papers ",node,qtdepublicacoes ,publicacoes 
            if (qtdepublicacoes >= self.min_papers):
                others =  set(n for n in nodesOrdered if n > node)
                for otherNode in others:
                    other_publicacoes = self.graph.edges(otherNode,data=False)
                    other_qtdepublicacoes = len(other_publicacoes)
                    if (other_qtdepublicacoes >= self.min_papers):
                        if (not self.graph.has_edge(node, otherNode)):
                            if self.USE_MAX_NUMBER_OF_PEOPLE_BETWEEN == True:
                                if networkx.has_path(self.graph, node, otherNode):
                                    shortestPathResult = networkx.shortest_path(self.graph, node, otherNode)
                                    #print shortestPathResult
                                    tamanho_caminho = len(shortestPathResult) - 1
                                    #print "%s ate %s: %s" %(node1, other_node,tamanho_caminho)
                                    #print repr(networkx.shortest_path(graph, node1, other_node));
                                    if ( tamanho_caminho > 0 ) and (tamanho_caminho <= self.MAX_NUMBER_OF_PEOPLE_BETWEEN ): # -2 porque inclui o inicio e fim
                                        #print "adicionando %s - %s" %(node, otherNode)
                                        results.append([node, otherNode])
                            else:
                                results.append([node, otherNode])
                
        print "getting pair of nodes that is not liked finished", datetime.today()
        return results
    
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
    

    def __init__(self, graph, min_papers = 1, USE_MAX_NUMBER_OF_PEOPLE_BETWEEN = False, MAX_NUMBER_OF_PEOPLE_BETWEEN = 6):
        
        self.graph = graph
        self.min_papers = min_papers
        self.USE_MAX_NUMBER_OF_PEOPLE_BETWEEN = USE_MAX_NUMBER_OF_PEOPLE_BETWEEN
        self.MAX_NUMBER_OF_PEOPLE_BETWEEN = MAX_NUMBER_OF_PEOPLE_BETWEEN
        
        #myfile = Formating.get_abs_file_path(filepathNodesToCalculate)
        #if not os.path.exists(myfile):
        #    with open(myfile, 'w') as fnodes:
        #        if allNodes:
        #            self.get_all_pair_nodes(graph, fnodes)
        #       else:
        #            self.get_pair_nodes_not_linked(graph,fnodes, min_papers)
        #        fnodes.close()
        #else:
        #    print "Nodes not linked file already generated. please delete if you want a new one.", datetime.today()
                 
            
        