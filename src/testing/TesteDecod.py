'''
Created on 22 de mai de 2016

@author: Administrador
'''
from unidecode import unidecode
import codecs


if __name__ == '__main__':
    arquivo = open('/grafos/hepth_data.ascii.2010.txt','r')
    arquivo2 = open('/grafos/hepth_data.ascii2.2010.txt','w')
    
    for linha in arquivo:
        arquivo2.write(linha)
    arquivo.close()
    arquivo2.close()
        