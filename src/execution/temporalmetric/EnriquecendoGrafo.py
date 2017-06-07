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


def converter(texto):
    dado = texto.replace('~', '')
    dado = dado.replace('{', '')
    dado = dado.replace('}', '')
    dado = dado.replace('}', '')
    dado = dado.replace('/', '')
    dado = dado.replace('\\', '')
    dado = dado.replace('"', '')
    dado = dado.replace('*', '')
    return dado.strip()

def gerar_grafo(years, base, graph):
    
    for year in years:
        basepath = '/home/cmuniz/execMen/grafos/'
        
        arxivFile = basepath + base + '_data.'+ str(year)  + '.txt'
        if os.path.isfile(arxivFile):
            arquivo = open(arxivFile, 'r')
            for line in arquivo:
                cols = line.split('\t')
                if len(cols) == 5:
                    keywords_not_clean = eval(cols[3])
                    keywords = set()
                    for k in keywords_not_clean:
                        keywords.add(k)
                    
                    myVertices = sorted(eval(cols[4]))
                    arxivAutores = []
                    for a in myVertices:
                        #arxivAutores.append(str.upper(a.split(' ')[0][0]) + '_' +  str.upper(convert(a.split(' ')[len(a.split(' '))-1])))
                        #arxivAutores.append(unicodedata.normalize('NFKD', str(a)).encode('ascii','ignore'))
                        author = converter(a)
                        if author != '':
                            arxivAutores.append(author)
                        #arxivAutores.append(converter(str.upper(a.decode('utf-8'))))
                    gerar_dados_grafo(graph, year, str(cols[0]), arxivAutores, keywords)
                       
            
        
    
def gerar_dados_grafo(graph, time, id_edge, autores, keywords):
    try:
        myAresta = { 'id_edge': id_edge,  'time' : int(time), 'keywords' : repr(keywords) }
        if len(autores) == 1:
            graph.add_edge(autores[0].strip(), autores[0].strip(),attr_dict=myAresta)
            
        for autor in autores:
            outrosAutores =  set(n for n in autores if n > autor)
            if (len(outrosAutores) == 0):
                graph.add_edge(autor.strip(), autor.strip(),attr_dict=myAresta)
               
            for outro in outrosAutores:
                graph.add_edge(autor.strip(), outro.strip(),attr_dict=myAresta)
    except:
        print "Unexpected error:"
        raise

def save_nodes(nodes,base):
    basepath = '/home/cmuniz/execMen/grafos/'
        
    arxivFile = basepath + base + '-2010-2015-arxiv-nodes.txt'
    file = codecs.open(arxivFile,'w', encoding='utf-8')
    for node in nodes:
        file.write(node)
        file.write('\n')
    file.close()
        
        

def gerar(base):
    graph = networkx.MultiGraph()
    gerar_grafo([1994,1995,1996,1997,1998,1999],base,graph)
    save_nodes(sorted(graph.nodes()),base)
    basepath = '/home/cmuniz/execMen/grafos/'
    networkx.write_graphml(graph, basepath + base + '-1994-1999-arxiv-graph.txt') 
    
def gerarteste(base):
    graph = networkx.MultiGraph()
    gerar_grafo([1994],base,graph)
    save_nodes(sorted(graph.nodes()),base)
    basepath = '/home/cmuniz/execMen/grafos/'
    networkx.write_graphml(graph, basepath + base + '-1994-new-graph.txt') 


if __name__ == '__main__':
    #print "gerando teste grafo grqc", datetime.now()
    #gerarteste('grqc')
    #print "gerando grafo grqc", datetime.now()
    #gerar('grqc')
    #print "gerando grafo hepth", datetime.now()
    #gerar('hepth')
    print "gerando grafo hepph", datetime.now()
    gerar('hepph')
    #print "gerando grafo condmat", datetime.now()
    #gerar('condmat')
    #print "gerando grafo astroph", datetime.now()
    #gerar('astroph')
    
    
    
    
    
    
    
    
        
    
            
   
    
