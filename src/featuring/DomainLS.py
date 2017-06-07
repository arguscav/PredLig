'''
Created on Jun 16, 2015

@author: cptullio
'''
from featuring.FeatureBase import FeatureBase
import networkx
from datetime import datetime


class DomainLS(FeatureBase):
    '''
    Original Link Score Defined by Chateuar
    '''
    def __repr__(self):
        return 'DLS'
    
    def getName(self):
        return 'DLS' 
     
    def __init__(self):
        super(DomainLS, self).__init__()
        
    
    
    def execute(self, node1, node2):
        datainicio = datetime.today()
        print "executando Domainls ", node1, node2, datainicio
        if not networkx.has_path(self.graph, node1, node2):
            return 0
        total = float(0)
        AllPaths = self.getAllShortestPath(node1, node2)
        SomatorioTPI = float(0)
        for path in AllPaths:
            nodesinPath = set();
            for pairofNodes in path:
                    nodesinPath.add(pairofNodes[0])
                    nodesinPath.add(pairofNodes[1])
                
            #print 'Caminho a ser analisado', path
            
            if len(path) <2:
                #print "NOT POSSIBLE TO CALCULATED!!  Path Length: " + str(len(path))
                continue
            yearActive = set()
            for node in nodesinPath:
                objectsinNode = self.get_ObjectsofNode(self.graph, node)
                yearActive.add(max(list(x['time'] for x in objectsinNode)))
            #print 'Active Years', yearActive    
            mediaYear = sum(yearActive)/len(yearActive)
            #print 'media Year', mediaYear
            k =  int(self.parameter.t1_)  - mediaYear
            #print "k: ", k 
            decay_value = self.parameter.decay ** k
            #print "decay value: " , decay_value
            m = len(path)
            sumofPublications = float(0)
            yearsOfPublicationLinks = []
            bagofWordsinPairs = []
            for pairofNodes in path:
                objectsinLinks = self.get_ObjectsofLinks(self.graph, pairofNodes[0], pairofNodes[1])
                #print "objetos localizados", objectsinLinks
                yearsOfPublicationLinks.append(max(list(x['time'] for x in objectsinLinks)))
                sumofPublications = sumofPublications + (1 / float(len(objectsinLinks)))
                bagofWordsNode1 = set()
                for t1 in objectsinLinks:
                    for bt1 in t1['keywords']:
                        bagofWordsNode1.add(bt1)
                bagofWordsinPairs.append(bagofWordsNode1);
            #calculating JC from path
            jcinPath = []
            for index in range(len(bagofWordsinPairs)-1):
                jcinPath.append(self.get_jacard_domain(bagofWordsinPairs[index] , bagofWordsinPairs[index+1] ) )
                
            hm = m / sumofPublications
            #print "Media Harmonica: ", hm
            numeradorTPI = hm * decay_value
            #print "Numerador TPI", numeradorTPI
            #print "Year of Publications:",  yearsOfPublicationLinks
            denominadorTPI = abs( int(self.parameter.t1_)  - max(yearsOfPublicationLinks )   ) + 1
            #print "Denominador TPI", denominadorTPI
            mediajc = sum(jcinPath) / float(len(jcinPath))
            #print "Media JC", mediajc
            TPI = numeradorTPI / (denominadorTPI * (self.parameter.domain_decay**mediajc))
            
            
            
            #print "TPI: ", TPI 
            
            SomatorioTPI = SomatorioTPI + TPI
            #print "TPI: ", TPI 
            
        TPI_L = SomatorioTPI / float(len(AllPaths)) 
        LINKSCORE = TPI_L /  (len(self.getShortestPath(node1, node2)) -1)
        #print "LINK SCORE: ", LINKSCORE    
        print "fim da executando Domain ls ", node1, node2, (datetime.today() - datainicio)
        return LINKSCORE     
            
        