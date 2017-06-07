'''
Created on 12 de jun de 2016

@author: Administrador
'''
import networkx
import numpy
from formating.arxiv.Formating import Formating

class CalculatingCombinationOnlyNowell(object):
    
    def all_neighbors(self, node):
        return set(networkx.all_neighbors(self.myparams.trainnigGraph, node))
    
    def get_common_neighbors(self, node1, node2):
        neighbors_node_1 = self.all_neighbors(node1)
        neighbors_node_2 = self.all_neighbors(node2)
        return neighbors_node_1.intersection(neighbors_node_2)    
    
    def get_ObjectsofLinks(self, graph, node1, node2):
        T3 = list(edge for n1, n2, edge in graph.edges([node1, node2], data=True) if ((n1 == node1 and n2 == node2) or (n1 == node2 and n2 == node1)) )
        return  T3
    
    def get_jacard_domain(self, bagofWordsNode1, bagofWordsNode2):
        f = (float)(len(bagofWordsNode1.intersection(bagofWordsNode2)))
        x = (float)(len(bagofWordsNode1.union(bagofWordsNode2)))
        if x == 0:
            return 0
        return f/x
    
    
    
    def get_TotalSucess(self):
        Sucess =  len(  list([n1,n2] for n1,n2,result in self.Analise if result ==1 ) )
        return {'sucess':Sucess}
    
    
    def AnalyseNodesInFuture(self, ordering, TestGraph):
        self.Analise = []
        for nodeToCheck in ordering:
            if (TestGraph.has_edge(nodeToCheck['node1'],nodeToCheck['node2'])):
                self.Analise.append([  nodeToCheck['node1'],nodeToCheck['node2'], 1 ])
            else:
                self.Analise.append([  nodeToCheck['node1'],nodeToCheck['node2'], 0 ])
            
            
             
    def normalize(self, data, max, min):
        if min == max:
            return data
        xnormalize = ((data - min)/(max - min))
        return xnormalize
    
    def ordering(self, topRank, normaliza = False):
        orderedResults = []
        CN = sorted(self.results, key=lambda value: value['combination'], reverse=True)
        for item in range(topRank):
            orderedResults.append({'node1':  CN[item]['node1'], 'node2':  CN[item]['node2'], 'combination':  CN[item]['combination'] })
    
        return orderedResults
    
    
    def combination(self, calculations, normalize = True):
        valueCN = float(0)
        valueJC = float(0)
        valueAAS = float(0)
        valuePA = float(0)
        valueTS08 = float(0)
        valueTS05 = float(0)
        valueTS02 = float(0)
        
        
        for item in calculations:
            if normalize:
                valueCN = self.normalize(item['cn'], self.maxCN, self.minCN) * self.weights['cn']
                valueJC = self.normalize(item['jc'], self.maxJC, self.minJC) * self.weights['jc']
                valueAAS = self.normalize(item['aas'], self.maxAAS, self.minAAS) * self.weights['aas']
                valuePA = self.normalize(item['pa'], self.maxPA, self.minPA) * self.weights['pa']
                valueTS08 = self.normalize(item['ts08'], self.maxTS08, self.minTS08) * self.weights['ts08']
                valueTS05 = self.normalize(item['ts05'], self.maxTS05, self.minTS05) * self.weights['ts05']
                valueTS02 = self.normalize(item['ts02'], self.maxTS02, self.minTS02) * self.weights['ts02']
            else:
                valueCN = item['cn'] * self.weights['cn']
                valueJC = item['jc'] * self.weights['jc']
                valueAAS = item['aas'] * self.weights['aas']
                valuePA = item['pa'] * self.weights['pa']
                valueTS08 = item['ts08'] * self.weights['ts08']
                valueTS05 = item['ts05'] * self.weights['ts05']
                valueTS02 = item['ts02'] * self.weights['ts02']
            if self.WillCombinate:
                self.results.append({'node1': item['node1'], 'node2': item['node2'], 'combination': (valueAAS+valueCN+valueJC+valuePA+valueTS02+valueTS05+valueTS08) })
            else:
                self.results.append({'node1': item['node1'], 'node2': item['node2'], 'cn' : valueCN, 'aas' : valueAAS, 'jc' : valueJC, 'pa' : valuePA, 'ts08' : valueTS08,'ts05' : valueTS05,'ts02' : valueTS02 })
      
    
    
    def __init__(self, myparams, nodesnotlinked, weights, WillCombinate):
        self.myparams = myparams
        self.weights = weights
        self.WillCombinate = WillCombinate
        qtyofNodesToProcess = len(nodesnotlinked)
        element = 0
        calcutations = []
        self.results = []
        self.minCN = float(0)
        self.maxCN = float(0)
        self.minAAS = float(0)
        self.maxAAS = float(0)
        self.minJC = float(0)
        self.maxJC = float(0)
        self.minPA = float(0)
        self.maxPA = float(0)
        self.minTS08 = float(0)
        self.maxTS08 = float(0)
        self.minTS05 = float(0)
        self.maxTS05 = float(0)
        self.minTS02 = float(0)
        self.maxTS02 = float(0)
        
        
        
        for pair in nodesnotlinked:
            element = element+1
            Formating.printProgressofEvents(element, qtyofNodesToProcess, "Calculating features for nodes not liked: ")
            neighbors_node1 = self.all_neighbors(pair[0])
            neighbors_node2 = self.all_neighbors(pair[1])
            CommonNeigbors = neighbors_node1.intersection(neighbors_node2)
            CommonNeigbors_Feature = len(CommonNeigbors)
            AAS_Feature = 0
            JC_Feature = 0
            PA_Feature = len(neighbors_node1) * len(neighbors_node2)
            TS_Feature08 = float(0)
            TS_Feature05 = float(0)
            TS_Feature02 = float(0)
            
            DTS_Feature = float(0)
            
            if CommonNeigbors_Feature > 0:
                print "Calculando ", pair[0], pair[1], CommonNeigbors_Feature
                x = (float)(len(neighbors_node1.union(neighbors_node2)))
                if x > 0:
                    JC_Feature = CommonNeigbors_Feature/x
                for pair_common_neighbor in CommonNeigbors:
                    secondary_neighbors = self.all_neighbors(pair_common_neighbor)
                    AAS_Feature += 1 / (numpy.log10(len(secondary_neighbors)) + 0.00001)
                
                    objectsNode1 = self.get_ObjectsofLinks(myparams.trainnigGraph, pair[0], pair_common_neighbor)
                    objectsNode2 = self.get_ObjectsofLinks(myparams.trainnigGraph, pair[1], pair_common_neighbor)
                    hm = 2 / ((1/float(len(objectsNode1))) + (1/float(len(objectsNode2))))
                    timesofLinksNode1 = []
                    timesofLinksNode2 = []
                  
                    for t1 in objectsNode1:
                        timesofLinksNode1.append(t1['time'])
                    for t2 in objectsNode2:
                        timesofLinksNode2.append(t2['time'])
                  
                    timesofLinksNode1.sort(reverse=True)
                    timesofLinksNode2.sort(reverse=True)
                    timeofLinks = timesofLinksNode1 + timesofLinksNode2
                    k =  int(self.myparams.t0_)  - int(max(timeofLinks))
                    decayfunction08 = (1 - 0.8) ** k
                    decayfunction05 = (1 - 0.5) ** k
                    decayfunction02 = (1 - 0.2) ** k
                    
                    control = (abs( max(timesofLinksNode1) - max(timesofLinksNode2) ) + 1)
                    ts08 = (hm * decayfunction08) / control
                    ts05 = (hm * decayfunction05) / control
                    ts02 = (hm * decayfunction02) / control
                    
                    TS_Feature08 = TS_Feature08 + ts08
                    TS_Feature05 = TS_Feature05 + ts05
                    TS_Feature02 = TS_Feature02 + ts02
                    
                    
                    
             
            if CommonNeigbors_Feature < self.minCN:
                self.minCN = CommonNeigbors_Feature
            if CommonNeigbors_Feature > self.maxCN:
                self.maxCN = CommonNeigbors_Feature
            
            if AAS_Feature < self.minAAS:
                self.minAAS = AAS_Feature
            if AAS_Feature > self.maxAAS:
                self.maxAAS = CommonNeigbors_Feature
            
            if PA_Feature < self.minPA:
                self.minPA = PA_Feature
            if PA_Feature > self.maxPA:
                self.maxPA = PA_Feature
            
            if JC_Feature < self.minJC:
                self.minJC = JC_Feature
            if JC_Feature > self.maxJC:
                self.maxJC = JC_Feature
            
            if TS_Feature08 < self.minTS08:
                self.minTS08 = TS_Feature08
            if TS_Feature08 > self.maxTS08:
                self.maxTS08 = TS_Feature08
            
            if TS_Feature05 < self.minTS05:
                self.minTS05 = TS_Feature05
            if TS_Feature05 > self.maxTS05:
                self.maxTS05 = TS_Feature05
            
            if TS_Feature02 < self.minTS02:
                self.minTS02 = TS_Feature02
            if TS_Feature02 > self.maxTS02:
                self.maxTS02 = TS_Feature02
                    
            calcutations.append({'node1' : pair[0], 'node2': pair[1], 'cn' : CommonNeigbors_Feature, 'aas' : AAS_Feature, 'jc' : JC_Feature, 'pa' : PA_Feature, 'ts08' : TS_Feature08,'ts05' : TS_Feature05,'ts02' : TS_Feature02, 'dts'  : DTS_Feature })
        
        self.combination(calcutations)    
                
        