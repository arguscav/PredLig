'''
Created on 12 de jun de 2016

@author: Administrador
'''
import networkx
import numpy
from formating.arxiv.Formating import Formating

class CalculatingTogetherCTimeScore(object):
    
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
        
        TS01 =  len(  list([n1,n2] for n1,n2,result in self.TS01 if result ==1 ) )
        TS02 =  len(  list([n1,n2] for n1,n2,result in self.TS02 if result ==1 ) )
        TS03 =  len(  list([n1,n2] for n1,n2,result in self.TS03 if result ==1 ) )
        TS04 =  len(  list([n1,n2] for n1,n2,result in self.TS04 if result ==1 ) )
        TS05 =  len(  list([n1,n2] for n1,n2,result in self.TS05 if result ==1 ) )
        TS06 =  len(  list([n1,n2] for n1,n2,result in self.TS06 if result ==1 ) )
        TS07 =  len(  list([n1,n2] for n1,n2,result in self.TS07 if result ==1 ) )
        TS08 =  len(  list([n1,n2] for n1,n2,result in self.TS08 if result ==1 ) )
        TS09 =  len(  list([n1,n2] for n1,n2,result in self.TS09 if result ==1 ) )
        
        result =  "\n" + str(TS01) + "\n" + str(TS02) + "\n" + str(TS03) + "\n" + str(TS04) 
        result = result + "\n" + str(TS05) + "\n" + str(TS06) + "\n" + str(TS07) + "\n" + str(TS08) 
        result = result + "\n" + str(TS09)

        return result
        
    
    
    def AnalyseNodesInFuture(self, ordering, TestGraph):
        self.TS01 = []
        self.TS02 = []
        self.TS03 = []
        self.TS04 = []
        self.TS05 = []
        self.TS06 = []
        self.TS07 = []
        self.TS08 = []
        self.TS09 = []
        
        for nodeToCheck in ordering:
            if (TestGraph.has_edge(nodeToCheck['TS09']['node1'],nodeToCheck['TS09']['node2'])):
                self.TS09.append([  nodeToCheck['TS09']['node1'],nodeToCheck['TS09']['node2'], 1 ])
            else:
                self.TS09.append([  nodeToCheck['TS09']['node1'],nodeToCheck['TS09']['node2'], 0 ])
            
            if (TestGraph.has_edge(nodeToCheck['TS08']['node1'],nodeToCheck['TS08']['node2'])):
                self.TS08.append([  nodeToCheck['TS08']['node1'],nodeToCheck['TS08']['node2'], 1 ])
            else:
                self.TS08.append([  nodeToCheck['TS08']['node1'],nodeToCheck['TS08']['node2'], 0 ])
            
            if (TestGraph.has_edge(nodeToCheck['TS07']['node1'],nodeToCheck['TS07']['node2'])):
                self.TS07.append([  nodeToCheck['TS07']['node1'],nodeToCheck['TS07']['node2'], 1 ])
            else:
                self.TS07.append([  nodeToCheck['TS07']['node1'],nodeToCheck['TS07']['node2'], 0 ])
            
            if (TestGraph.has_edge(nodeToCheck['TS06']['node1'],nodeToCheck['TS06']['node2'])):
                self.TS06.append([  nodeToCheck['TS06']['node1'],nodeToCheck['TS06']['node2'], 1 ])
            else:
                self.TS06.append([  nodeToCheck['TS06']['node1'],nodeToCheck['TS06']['node2'], 0 ])
            
            if (TestGraph.has_edge(nodeToCheck['TS05']['node1'],nodeToCheck['TS05']['node2'])):
                self.TS05.append([  nodeToCheck['TS05']['node1'],nodeToCheck['TS05']['node2'], 1 ])
            else:
                self.TS05.append([  nodeToCheck['TS05']['node1'],nodeToCheck['TS05']['node2'], 0 ])
            
            
            if (TestGraph.has_edge(nodeToCheck['TS04']['node1'],nodeToCheck['TS04']['node2'])):
                self.TS04.append([  nodeToCheck['TS04']['node1'],nodeToCheck['TS04']['node2'], 1 ])
            else:
                self.TS04.append([  nodeToCheck['TS04']['node1'],nodeToCheck['TS04']['node2'], 0 ])
            
            if (TestGraph.has_edge(nodeToCheck['TS03']['node1'],nodeToCheck['TS03']['node2'])):
                self.TS03.append([  nodeToCheck['TS03']['node1'],nodeToCheck['TS03']['node2'], 1 ])
            else:
                self.TS03.append([  nodeToCheck['TS03']['node1'],nodeToCheck['TS03']['node2'], 0 ])
            
            if (TestGraph.has_edge(nodeToCheck['TS02']['node1'],nodeToCheck['TS02']['node2'])):
                self.TS02.append([  nodeToCheck['TS02']['node1'],nodeToCheck['TS02']['node2'], 1 ])
            else:
                self.TS02.append([  nodeToCheck['TS02']['node1'],nodeToCheck['TS02']['node2'], 0 ])
            
            if (TestGraph.has_edge(nodeToCheck['TS01']['node1'],nodeToCheck['TS01']['node2'])):
                self.TS01.append([  nodeToCheck['TS01']['node1'],nodeToCheck['TS01']['node2'], 1 ])
            else:
                self.TS01.append([  nodeToCheck['TS01']['node1'],nodeToCheck['TS01']['node2'], 0 ])
            
            
            
             
    def normalize(self, data, max, min):
        if min == max:
            return data
        xnormalize = ((data - min)/(max - min))
        return xnormalize
    
    def saving_orderedResult(self, filepath, ordering):
     
        fcn = open(Formating.get_abs_file_path(filepath + '.cn.txt') , 'w')
        fpa = open(Formating.get_abs_file_path(filepath + '.pa.txt') , 'w')
        faas = open(Formating.get_abs_file_path(filepath + '.aas.txt') , 'w')
        fjc = open(Formating.get_abs_file_path(filepath + '.jc.txt') , 'w')
        fts05 = open(Formating.get_abs_file_path(filepath + '.ts05.txt') , 'w')
        fdts05 = open(Formating.get_abs_file_path(filepath + '.dts05.txt') , 'w')
    
        for item_result in ordering:
            fcn.write(repr(item_result['cn']['node1']) + ';' + repr(item_result['cn']['node2']) +';' + repr(item_result['cn']['cn'])     + '\n')
            faas.write(repr(item_result['aas']['node1']) + ';' + repr(item_result['aas']['node2']) +';' + repr(item_result['aas']['aas'])     + '\n')
            fjc.write(repr(item_result['jc']['node1']) + ';' + repr(item_result['jc']['node2']) +';' + repr(item_result['jc']['jc'])     + '\n')
            fpa.write(repr(item_result['pa']['node1']) + ';' + repr(item_result['pa']['node2']) +';' + repr(item_result['pa']['pa'])     + '\n')
            fts05.write(repr(item_result['ts05']['node1']) + ';' + repr(item_result['ts05']['node2']) +';' + repr(item_result['ts05']['ts05'])     + '\n')
            fdts05.write(repr(item_result['dts05']['node1']) + ';' + repr(item_result['dts05']['node2']) +';' + repr(item_result['dts05']['dts05'])     + '\n')
            
        fcn.close() 
        fpa.close()
        faas.close()
        fjc.close()
        fts05.close()
        fdts05.close()  
        
    
    def ordering(self, topRank, normaliza = False):
        orderedResults = []
        
        TS09 = sorted(self.results, key=lambda value: value['TS09'], reverse=True)
        
        TS08 = sorted(self.results, key=lambda value: value['TS08'], reverse=True)
        
        TS07 = sorted(self.results, key=lambda value: value['TS07'], reverse=True)
        
        TS06 = sorted(self.results, key=lambda value: value['TS06'], reverse=True)
        
        TS05 = sorted(self.results, key=lambda value: value['TS05'], reverse=True)
        
        TS04 = sorted(self.results, key=lambda value: value['TS04'], reverse=True)
        
        TS03 = sorted(self.results, key=lambda value: value['TS03'], reverse=True)
        
        TS02 = sorted(self.results, key=lambda value: value['TS02'], reverse=True)
        
        TS01 = sorted(self.results, key=lambda value: value['TS01'], reverse=True)
        
        
        for item in range(topRank):
            orderedResults.append({'TS09' : TS09[item], 'TS08' : TS08[item], 'TS07' : TS07[item], 'TS06' : TS06[item], 'TS05' : TS05[item],'TS04' : TS04[item],'TS03' : TS03[item], 'TS02'  : TS02[item], 'TS01'  : TS01[item] })
    
        return orderedResults
    
    def calculateLS(self, node1, node2, allPaths):
        print node1,node2, allPaths
    
    def __init__(self, myparams, nodesnotlinked):
        self.myparams = myparams
        qtyofNodesToProcess = len(nodesnotlinked)
        element = 0
        self.results = []
        
        for pair in nodesnotlinked:
            element = element+1
            Formating.printProgressofEvents(element, qtyofNodesToProcess, "Calculating features for nodes not liked: ")
            neighbors_node1 = self.all_neighbors(pair[0])
            neighbors_node2 = self.all_neighbors(pair[1])
            len_neihbors_node1 = len(neighbors_node1)
            len_neihbors_node2 = len(neighbors_node2)
            CommonNeigbors = neighbors_node1.intersection(neighbors_node2)
            CommonNeigbors_Feature = len(CommonNeigbors)
            TS_Feature09 = float(0)
            TS_Feature08 = float(0)
            TS_Feature07 = float(0)
            TS_Feature06 = float(0)
            TS_Feature05 = float(0)
            TS_Feature04 = float(0)
            TS_Feature03 = float(0)
            TS_Feature02 = float(0)
            TS_Feature01 = float(0)
            
            if CommonNeigbors_Feature > 0:
                print "Calculando ", pair[0], pair[1], CommonNeigbors_Feature
                #x = (float)(len(neighbors_node1.union(neighbors_node2)))
                #if x > 0:
                #    JC_Feature = CommonNeigbors_Feature/x
                for pair_common_neighbor in CommonNeigbors:
                    #secondary_neighbors = self.all_neighbors(pair_common_neighbor)
                    #AAS_Feature += 1 / (numpy.log10(len(secondary_neighbors)) + 0.00001)
                
                    objectsNode1 = self.get_ObjectsofLinks(myparams.trainnigGraph, pair[0], pair_common_neighbor)
                    objectsNode2 = self.get_ObjectsofLinks(myparams.trainnigGraph, pair[1], pair_common_neighbor)
                    
                    hm = 2 / ( (1/float(len(objectsNode1))) + (1/float(len(objectsNode2))))
                    #print pair[0], pair_common_neighbor, "Media Harmonica ", hm 
                    
                    timesofLinksNode1 = []
                    timesofLinksNode2 = []
                    bagofWordsNode1 = set()
                    bagofWordsNode2 = set()
            
                    for t1 in objectsNode1:
                        timesofLinksNode1.append(t1['time'])
                        for b1 in eval(t1['keywords']):
                            bagofWordsNode1.add(b1)
                    for t2 in objectsNode2:
                        timesofLinksNode2.append(t2['time'])
                        for b2 in eval(t2['keywords']):
                            bagofWordsNode2.add(b2)
                       
            
                    timesofLinksNode1.sort(reverse=True)
                    timesofLinksNode2.sort(reverse=True)
                    timeofLinks = timesofLinksNode1 + timesofLinksNode2
                    
                    #print  pair_common_neighbor, "publicacoes realizadas: ", timeofLinks 
                    
                    k =  int(self.myparams.t0_)  - int(max(timeofLinks))
                    
                    #print  pair_common_neighbor, "K ", k 
                    #decayfunction09 = (0.9) ** k
                    #decayfunction08 = (0.8) ** k
                    #decayfunction07 = (0.7) ** k
                    #decayfunction06 = (0.6) ** k
                    #decayfunction05 = (0.5) ** k
                    decayfunction04 = (0.9) ** k
                    #decayfunction03 = (0.3) ** k
                    #decayfunction02 = (0.2) ** k
                    #decayfunction01 = (0.1) ** k
                    
                    #print  pair_common_neighbor, "funcao de decaimento 0.5 ", decayfunction05 
                    
                    
                    control = ( abs( max(timesofLinksNode1) - max(timesofLinksNode2) ) + 1)
                    
                    jcDomain = self.get_jacard_domain(bagofWordsNode1, bagofWordsNode2)
                    
                    #print  pair_common_neighbor, "denominador inicial considerando apenas TS ", control 
                     
                    ts09 = (hm * decayfunction04) /  (control * ((0.9) ** jcDomain))
                    ts08 = (hm * decayfunction04) /  (control * ((0.8) ** jcDomain))
                    ts07 = (hm * decayfunction04) /  (control * ((0.7) ** jcDomain))
                    ts06 = (hm * decayfunction04) /  (control * ((0.6) ** jcDomain))
                    ts05 = (hm * decayfunction04) /  (control * ((0.5) ** jcDomain))
                    ts04 = (hm * decayfunction04) /  (control * ((0.4) ** jcDomain))
                    ts03 = (hm * decayfunction04) /  (control * ((0.3) ** jcDomain))
                    ts02 = (hm * decayfunction04) /  (control * ((0.2) ** jcDomain))
                    ts01 = (hm * decayfunction04) /  (control * ((0.1) ** jcDomain))
                    
                    #print  pair_common_neighbor, "TS ", ts05 
                    TS_Feature09 = TS_Feature09 + ts09
                    TS_Feature08 = TS_Feature08 + ts08
                    TS_Feature07 = TS_Feature07 + ts07
                    TS_Feature06 = TS_Feature06 + ts06
                    TS_Feature05 = TS_Feature05 + ts05
                    TS_Feature04 = TS_Feature04 + ts04
                    TS_Feature03 = TS_Feature03 + ts03
                    TS_Feature02 = TS_Feature02 + ts02
                    TS_Feature01 = TS_Feature01 + ts01
                    
                    #print  pair_common_neighbor, "conjuntos de palavras ", bagofWordsNode1, bagofWordsNode2 
                    
                    
                    
                    #print  pair_common_neighbor, "JC ", jcDomain 
                    
                    #dts02 = (hm * decayfunction02) /  (control * ((0.2) ** jcDomain))
                    #dts05 = (hm * decayfunction02) /  (control * ((0.5) ** jcDomain))
                    #dts08 = (hm * decayfunction02) /  (control * ((0.8) ** jcDomain))
                    
                    #print  pair_common_neighbor, "DTS ", dts05 
                    
                    #DTS_Feature02 = DTS_Feature02 + dts02
                    #DTS_Feature05 = DTS_Feature05 + dts05
                    #DTS_Feature08 = DTS_Feature08 + dts08
                
                
                
                
            self.results.append({'node1' : pair[0], 'node2': pair[1], 'TS09' : TS_Feature09, 'TS08' : TS_Feature08, 'TS07' : TS_Feature07, 'TS06' : TS_Feature06, 'TS05' : TS_Feature05,'TS04' : TS_Feature04,'TS03' : TS_Feature03, 'TS02'  : TS_Feature02, 'TS01'  : TS_Feature01 })
                
                
        