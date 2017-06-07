'''
Created on Aug 22, 2015

@author: cptullio
Analysing the results
'''
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from calculating.Calculate import Calculate
from analysing.Analyse import Analyse
from calculating.VariableSelection import VariableSelection
from formating.FormatingDataSets import FormatingDataSets
import networkx
import mysql.connector

if __name__ == '__main__':
    util = ParameterUtil(parameter_file = 'data/formatado/arxiv/nowell_astroph_1994_1999.txt')
    myparams = Parameterization(util.keyword_decay, util.lengthVertex, util.t0, util.t0_, util.t1, util.t1_, util.FeaturesChoiced, util.graph_file, util.trainnig_graph_file, util.test_graph_file, util.decay)
    myparams.generating_Training_Graph()
    AllNodes = VariableSelection(myparams.trainnigGraph, util.nodes_file,util.min_edges, True)
    calc = Calculate(myparams, util.nodes_file, util.calculated_file, util.ordered_file, util.maxmincalculated_file)
    print 'armazenando resultados'
    cnx = mysql.connector.connect(user='root', password='1234',
                              host='127.0.0.1',
                              database='calculos')
    add_result = ("INSERT INTO resultadopesos "
               "(no1, no2, resultados) "
               "VALUES (%s, %s, %s)")
    cursor = cnx.cursor()
    calculatedFile = open(FormatingDataSets.get_abs_file_path(util.calculated_file), 'r')
    for linha in calculatedFile:
        dado = Calculate.reading_calculateLine(linha)
        data_result = (dado[1], dado[2].replace('\n',''),str(dado[0]))
        cursor.execute(add_result, data_result)
    calculatedFile.close()
    cnx.commit()
    cursor.close()
    cnx.close()
    
    