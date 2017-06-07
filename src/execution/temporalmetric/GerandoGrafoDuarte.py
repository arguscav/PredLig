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
import json
from pydblite import Base



      

if __name__ == '__main__':
#     palavrachavePath = '/Mestrado-2016/tabelas_dump/publicacaokeyword.csv'
#     palavrachaveArquivo = open(palavrachavePath, 'r')
#     
#     publicacaoPath = '/Mestrado-2016/tabelas_dump/publicacao.csv'
#     publicacaoArquivo = open(publicacaoPath, 'r')
#     
#     autoresPath = '/Mestrado-2016/tabelas_dump/autorpublicacao.csv'
#     autoresArquivo = open(autoresPath, 'r')
#     
    
    infoPath = '/Mestrado-2016/tabelas_dump/infoImportantes2000_2005.csv'
    infoArquivo = open(infoPath, 'w')
    
    infoArquivo.write('idpublication;year;keywords;authors\n')
    kdb = Base('/Mestrado-2016/tabelas_dump/palavra.pdl')
    kdb.open()
    kdb.create_index('idpublicacao')
    
    pdb = Base('/Mestrado-2016/tabelas_dump/publicacao.pdl')
    pdb.open()
    pdb.create_index('idpublicacao')
    
    adb = Base('/Mestrado-2016/tabelas_dump/autor.pdl')
    adb.open()
    adb.create_index('idpublicacao')
    
    pub = [r for r in pdb if r['ano'] >= 2000 and r['ano'] <= 2005 ]
    i = 0
    tamanho = len(pub)
    
    for row in pub:
        inicio = datetime.now()
        i = i + 1
        palavras =  set() 
        for p in kdb._idpublicacao[row['idpublicacao']]:
            palavras.add(p['idpalavrachave'])
        
        #palavras = set(r['idpalavrachave'] for r in kdb if  r['idpublicacao'] == row['idpublicacao'])
        autores = set()
        for p in adb._idpublicacao[row['idpublicacao']]:
            autores.add(p['idautor'])
        
        #autores = set(r['idautor'] for r in adb if  r['idpublicacao'] == row['idpublicacao'])
        infoArquivo.write(repr(row['idpublicacao']))
        infoArquivo.write(';')
        infoArquivo.write(repr(row['ano']))
        infoArquivo.write(';')
        infoArquivo.write(repr(palavras))
        infoArquivo.write(';')
        infoArquivo.write(repr(autores))
        infoArquivo.write('\n')
        
        print i,  ' of ', tamanho ,  datetime.now() - inicio
    infoArquivo.flush()
    infoArquivo.close()
        
         
        
        #for palava in kdb['idpublicacao'] == row['idpublicacao']:
        #    palavra.add(kdb(['idpalavrachave'])
        
#     kdb = Base('/Mestrado-2016/tabelas_dump/palavra.pdl')
#     kdb.create('idpublicacao', 'idpalavrachave')
#     i = 0
#     for line in palavrachaveArquivo:
#         i = i+1
#         if i > 1:
#             colunas = line.strip().split(';')
#             kdb.insert(int(colunas[1]),int(colunas[0]) )
#     kdb.commit()
#    print 'palavra chave importado! ', i
    
#     pdb = Base('/Mestrado-2016/tabelas_dump/publicacao.pdl')
#     pdb.create('idpublicacao', 'ano')
#     i = 0
#     for line in publicacaoArquivo:
#         i = i+1
#         if i > 1:
#             try:
#                 
#                 colunas = line.strip().split(';')
#                 pdb.insert(int(colunas[0]),int(colunas[(len(colunas)-1)]) )
#             except:
#                 print "erro importacao linha:  ", i
#     pdb.commit()
#     
#     print 'publicacao importado! ', i
#     
#     adb = Base('/Mestrado-2016/tabelas_dump/autor.pdl')
#     adb.create('idpublicacao', 'idautor')
#     i = 0
#     for line in autoresArquivo:
#         i = i+1
#         if i > 1:
#             colunas = line.strip().split(';')
#             adb.insert(int(colunas[0]),int(colunas[(len(colunas)-1)]) )
#     print 'autores importado! ', i
#     adb.commit()
    
    
#     
#     for line in publicacaoConteudo:
#         
#         colunas = line.strip().split(';')
#         i = i +1
#         if i > 1:
#             print "Importando Linha: ", i
#             idpublicacao = int(colunas[0])
#             ano = int(colunas[(len(colunas)-1)])
#             if ano > 0:
#                 palavrasChaves = getPalavras(idpublicacao)
#                 autores = getAutores(idpublicacao)
#                 infoArquivo.write(repr(idpublicacao))
#                 infoArquivo.write(';')
#                 infoArquivo.write(repr(ano))
#                 infoArquivo.write(';')
#                 infoArquivo.write(repr(palavrasChaves))
#                 infoArquivo.write(';')
#                 infoArquivo.write(repr(autores))
#                 infoArquivo.write('\n')
#     infoArquivo.flush()
#     infoArquivo.close()
