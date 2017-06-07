'''
Created on 21 de dez de 2015

@author: CarlosPM
'''
import networkx
import matplotlib
import os.path
import codecs
import unicodedata
from datetime import datetime

    
def gerar_dados_grafo(graph, time, id_edge, autores, keywords):
    try:
        myAresta = { 'id_edge': id_edge,  'time' : int(time), 'keywords' : repr(keywords) }
        if len(autores) == 1:
            graph.add_edge(autores[0], autores[0],attr_dict=myAresta)
            
        for autor in autores:
            outrosAutores =  set(n for n in autores if n > autor)
            if (len(outrosAutores) == 0):
                graph.add_edge(autor, autor,attr_dict=myAresta)
               
            for outro in outrosAutores:
                graph.add_edge(autor, outro,attr_dict=myAresta)
    except:
        print "Unexpected error:"
        raise


if __name__ == '__main__':
    print "gerando teste grafo grqc", datetime.now()
    graph = networkx.MultiGraph()
    
    infoPath = '/Mestrado-2016/tabelas_dump/infoImportantes1994_1999.csv'
    infoArquivo = open(infoPath, 'r')
    i = 0 
    for line in infoArquivo:
        i = i +1
        if i > 1:
            cols = line.split(';')
            id = eval(cols[0])
            ano = eval(cols[1])
            palavras = eval(cols[2])
            autores = sorted(eval(cols[3]))
            gerar_dados_grafo(graph, ano, id, autores, palavras)
            
            
    networkx.write_graphml(graph, 'duarte_1994_1999-new-graph.txt') 
    
    
    
    
    
    
    
    
        
    
            
   
    
