'''
Created on Jul 18, 2015

@author: cptullio
'''
import psycopg2
from formating.FormatingDataSets import FormatingDataSets
import networkx
from datetime import datetime


class DuarteFormattingOnlyIME(FormatingDataSets):
    
    
    def __init__(self, graphfile):
        self.Autors = []
        self.Publications = []
        self.AutorsPublicacao = []
        super(DuarteFormattingOnlyIME, self).__init__('', graphfile)
        
    
    def readingOrginalDataset(self):
        print "Starting Reading Original Dataset", datetime.today()
        con = None
        try:
            con = psycopg2.connect(database='projetomestrado', user='postgres', password='123456')
            
            curPublicacao = con.cursor()
            curPublicacao.execute("select distinct p.idpublicacao, p.titulo, p.ano from projetomestrado.publicacao p inner join projetomestrado.autorpublicacao a on a.idpublicacao = p.idpublicacao where a.idautor in (select idautor from projetomestrado.autor where afiliacao = 'Instituto Militar de Engenharia')")
            curPublicacaoData = curPublicacao.fetchall()
            element = 0
            qty = len(curPublicacaoData)
            print qty
            for linha in curPublicacaoData:
                element = element+1
                FormatingDataSets.printProgressofEvents(element, qty, "Adding paper to new graph: ")
            
                idpublicacao = linha[0]
                curPublicacaoPalavras = con.cursor()
                curPublicacaoPalavras.execute("select k.keyword from projetomestrado.keyword k inner join projetomestrado.publicacaokeyword pk on pk.idkeyword = k.idkeyword where pk.idpublicacao =" + str(idpublicacao))
                palavras = []
                for palavra in curPublicacaoPalavras.fetchall():
                    palavras.append(palavra[0].strip())
                curAutores = con.cursor()
                curAutores.execute("select a.idautor, a.primeironome, a.ultimonome from projetomestrado.autorpublicacao ap inner join projetomestrado.autor a on a.idautor = ap.idautor where ap.idpublicacao = "+ str(idpublicacao))
                autores = []
                for autor in curAutores.fetchall():
                    autores.append([autor[0], autor[1] + "," + autor[2]])
            
                    
                self.Publications.append([idpublicacao, linha[1], linha[2], palavras, autores ])
            
            self.Graph = networkx.Graph()
            
            for item_article in self.Publications:
                self.Graph.add_node('P_' + str(item_article[0]), {'node_type' : 'E', 'title' : item_article[1].decode("latin_1"), 'time' : int(item_article[2]), 'keywords': str(item_article[3]) })
                for item_autor in item_article[4]:
                    self.Graph.add_node(int(item_autor[0]), {'node_type' : 'N', 'name' : item_autor[1].decode("latin_1") })
                    self.Graph.add_edge('P_' + str(item_article[0]), int(item_autor[0]) )
            
            print "Reading Original Dataset finished", datetime.today()
            
            
    
            
            
            
            
        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
        finally:
            if con:
                con.close()
    
    
   
        
