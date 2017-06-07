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
from featuring.FeatureBase import FeatureBase
from featuring.CNFeature import CNFeature
from Canvas import Line


def getPairNodes(node1, node2, calculatedFile):
    
    result = None
    texto = str(node1) + '\t' + str(node2)
    textov2 = str(node2) + '\t' + str(node1)
    
    
    for line in calculatedFile:
        if texto in line:
            result = line
            break
        elif textov2 in line:
            result = line
            break
    calculatedFile.seek(0)
    return result
    

if __name__ == '__main__':
    util = ParameterUtil(parameter_file = 'data/formatado/arxiv/nowell_astroph_1994_1999.txt')
    calculatedFile = open(FormatingDataSets.get_abs_file_path(util.calculated_file), 'r')
    for linha in calculatedFile:
        x.append(Calculate.reading_calculateLine(linha))
    calculatedFile.close()
    myparams = Parameterization(util.keyword_decay, util.lengthVertex, util.t0, util.t0_, util.t1, util.t1_, util.FeaturesChoiced, util.graph_file, util.trainnig_graph_file, util.test_graph_file, util.decay)
    myparams.generating_Training_Graph()
    Nodes_notLinked = VariableSelection(myparams.trainnigGraph, util.nodes_notlinked_file,util.min_edges)
    nodes_notlinkedFile = open(FormatingDataSets.get_abs_file_path(util.nodes_notlinked_file), 'r')
    qtyLine = 0
    qtyCalculated = 0
    f = open(FormatingDataSets.get_abs_file_path(util.calculated_file )+ '.weight.txt', 'w')
    minValueCalculated = list(99999 for x in myparams.featuresChoice)
    maxValueCalculated = list(0 for x in myparams.featuresChoice)
    qtyFeatures = len(myparams.featuresChoice)
    for line in nodes_notlinkedFile:
        qtyLine = qtyLine + 1
        item = VariableSelection.getItemFromLine(line)
        
        qtyofnodesnotLinked = len(item[1])
        print 'Qtde of not linked itens', qtyofnodesnotLinked, ' in line ', qtyLine 
        for neighbor_node in item[1]:
            qtyCalculated = qtyCalculated + 1
            node1 = item[0]
            node2 = neighbor_node
            cn = util.FeaturesChoiced[0][0].get_common_neighbors(node1,node2)
            total = 0
            for c in cn:
                total = total + ( Calculate.reading_calculateLine(getPairNodes(node1, c, calculatedFile))[0][0] + Calculate.reading_calculateLine(getPairNodes(node2, c, calculatedFile))[0][0])
            
            for index_features in range(qtyFeatures):
                if total < minValueCalculated[index_features]:
                    minValueCalculated[index_features] = total
                if total > maxValueCalculated[index_features]:
                    maxValueCalculated[index_features] = total    
            valor = "{'[WTS, 1]': " + repr(total)  +  "}\t" + str(node1) +'\t'+ str(node2)+ '\n'
            f.write(valor)
        
    f.close()    
    fcontentMaxMin = open(FormatingDataSets.get_abs_file_path(util.maxmincalculated_file + '.weight.txt'), 'w')
    fcontentMaxMin.write(str(qtyCalculated) + '\t' + repr(minValueCalculated) + '\t' + repr(maxValueCalculated) )
    fcontentMaxMin.close()    
        
    #VariableSelection.getItemFromLine(util.nodes_notlinked_file)
    #f = CNFeature()
    #f.graph = myparams.trainnigGraph
    
    #pesos = list(x for x in weighgted_graph.edges(data=True) if (len(x[2]) != 0))
    #print pesos
    
    #wcnnode1 = list(eval(x[2]['weight']) for x in pesos if (x[0] == '3' and x[1] == '8') )[0]
    
    #wcnnode2 = list(eval(x[2]['weight']) for x in pesos if (x[0] == '7' and x[1] == '8') )[0]
    
    #print float(wcnnode1[1]) + float(wcnnode2[1])
        #if len(x[2]) != 0:
        #    print x[0], x[1], eval(x[2]['weight'])[1]
        #    print f.all_node_neighbors( x[0])
        #    print f.all_node_neighbors( x[1])
        #    print "____________________________"
    

    