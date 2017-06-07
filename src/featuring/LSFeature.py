'''
Created on Jun 16, 2015

@author: cptullio
'''
from featuring.FeatureBase import FeatureBase
import networkx
from datetime import datetime


class LSFeature(FeatureBase):
    '''
    Original Link Score Defined by Chateuar
    '''
    def __repr__(self):
        return 'LS'
    

    def getName(self):
        return 'LS' 

    def __init__(self):
        super(LSFeature, self).__init__()
        
    
    
    def execute(self, node1, node2):
        #datainicio = datetime.today()
        #print "executando ls ", node1, node2, datainicio
        if not networkx.has_path(self.graph, node1, node2):
            return 0
        total = float(0)
        AllPaths = self.getAllShortestPath(node1, node2)
        print "Calculo sobre os paths: ", len(AllPaths)
        SomatorioTPI = float(0)
        pairofNodesAlreadyCalculated = []
        for path in AllPaths:
            nodesinPath = set();
            for pairofNodes in path:
                    nodesinPath.add(pairofNodes[0])
                    nodesinPath.add(pairofNodes[1])
                
            #print nodesinPath
            if len(path) <2:
                continue
            
            valor = list(v for d,v in pairofNodesAlreadyCalculated if d==nodesinPath)
            if len(valor) == 1:
                SomatorioTPI = SomatorioTPI + valor[0]
            else:
            
                yearActive = set()
                for node in nodesinPath:
                    objectsinNode = self.get_ObjectsofNode(self.graph, node)
                    #print objectsinNode
                    yearActive.add(max(list(x['time'] for x in objectsinNode)))
                #print yearActive
                mediaYear = sum(yearActive)/len(yearActive)
                k =  int(self.parameter.t1_)  - mediaYear
                decay_value = self.parameter.decay ** k
                m = len(path)
                sumofPublications = float(0)
                yearsOfPublicationLinks = []
                for pairofNodes in path:
                    objectsinLinks = self.get_ObjectsofLinks(self.graph, pairofNodes[0], pairofNodes[1])
                    yearsOfPublicationLinks.append(max(list(x['time'] for x in objectsinLinks)))
                    sumofPublications = sumofPublications + (1 / float(len(objectsinLinks)))
                hm = m / sumofPublications
                numeradorTPI = hm * decay_value
                denominadorTPI = abs( int(self.parameter.t1_)  - max(yearsOfPublicationLinks )   ) + 1
                TPI = numeradorTPI / denominadorTPI
                
                SomatorioTPI = SomatorioTPI + TPI
            
        TPI_L = SomatorioTPI / float(len(AllPaths)) 
        LINKSCORE = TPI_L /  (len(self.getShortestPath(node1, node2)) -1)
        #print "fim da executando ls ", node1, node2, (datetime.today() - datainicio)
        #return LINKSCORE     
            
        