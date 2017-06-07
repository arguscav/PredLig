'''
Created on Jun 16, 2015

@author: cptullio
'''
import numpy
from formating.dblp.Formating import Formating
from datetime import datetime
from networkx.classes.function import neighbors
from formating.FormatingDataSets import FormatingDataSets
from calculating.VariableSelection import VariableSelection
import os
from _elementtree import Element
import gc
import networkx



class CalculateInMemory(object):
    
    
    def combinate_linear(self, resultsNormalized):
        result = []
        for resultNormalized in resultsNormalized:
            total = float(0)
            for index in range(len(self.preparedParameter.ScoresChoiced)):
                total = total + resultNormalized[2][index]
            result.append([resultNormalized[0],resultNormalized[1],total])
        return result
    
    def ordering_combinate_linear(self, topRank, resultsCombinate):
        scoreOrderedResult = []
        orderingByDesc = True
        scoreOrder = sorted(resultsCombinate, key=lambda value: value[2], reverse=orderingByDesc)
        for item in range(topRank):
            scoreOrderedResult.append( [scoreOrder[item][0], scoreOrder[item][1], scoreOrder[item][2]])
        return scoreOrderedResult
    
    
    
    def ordering(self, topRank, resultNormalized):
        #print 'a ser ordenado ', resultNormalized
        orderedResults = []
        
        for index in range(len(self.preparedParameter.ScoresChoiced)):
            scoreOrderedResult = []
            orderingByDesc = True
            if (self.preparedParameter.ScoresChoiced[index][2] == 1):
                orderingByDesc = False
            scoreOrder = sorted(resultNormalized, key=lambda value: value[2][index], reverse=orderingByDesc)
            
            #print 'Ordenado', scoreOrder
            for item in range(topRank):
                scoreOrderedResult.append( scoreOrder[item])
            orderedResults.append(scoreOrderedResult)
        return orderedResults
    
    def normalize(self, data, indice):
        if self.maxValueCalculated[indice] == self.minValueCalculated[indice]:
            return data
        xnormalize = (data - self.minValueCalculated[indice])/(self.maxValueCalculated[indice] - self.minValueCalculated[indice])
        return xnormalize            
     
    def normalizeResultsToCombine(self, results):
        for itemResult in results:
            for index_score in range(len(self.preparedParameter.ScoresChoiced)):
                itemResult[2][index_score] = (self.normalize( itemResult[2][index_score], index_score  ) * float(self.preparedParameter.ScoresChoiced[index_score][1]))
            
    def saving_calculateResult_normalized(self, filepath, results):
        f = open(Formating.get_abs_file_path(filepath), 'w')
        header = 'no1,no2'
        for index_score in range(len(self.preparedParameter.ScoresChoiced)):
            header = header + ',' + self.preparedParameter.ScoresChoiced[index_score][0].getName()
        f.write(header + '\n')
        
        for itemResult in results:
            value = ''
            for index_score in range(len(self.preparedParameter.ScoresChoiced)):
                value = value + ',' + repr(   self.normalize( itemResult[2][index_score], index_score  ) )
                
            f.write( itemResult[0] + ',' + itemResult[1] + value + '\n')
            
            
        f.close()  
        
    def saving_calculateResult(self, filepath, results):
        f = open(Formating.get_abs_file_path(filepath), 'w')
        header = 'no1,no2'
        for index_score in range(len(self.preparedParameter.ScoresChoiced)):
            header = header + ',' + self.preparedParameter.ScoresChoiced[index_score][0].getName()
        f.write(header + '\n')
        
        for itemResult in results:
            value = ''
            for index_score in range(len(self.preparedParameter.ScoresChoiced)):
                value = value + ',' + repr(   itemResult[2][index_score]  )
                
            f.write( itemResult[0] + ',' + itemResult[1] + value + '\n')
            
            
        f.close()   
        
        
        
        
    def saving_orderedResult(self, filepath, results):
        
        for index_score in range(len(results)):
            f = open(Formating.get_abs_file_path(filepath + str(self.preparedParameter.ScoresChoiced[index_score][0]) + '.txt') , 'w')
            for item_result in results[index_score]:
                f.write(repr(item_result[0]) + ";" + repr(item_result[1]) + ";" + repr(item_result[2][index_score]) + '\n')
            f.close()   
    
    def save_Max_min_file(self, filepath, qtyCalculated, minValues, maxValues):
        
        fcontentMaxMin = open(Formating.get_abs_file_path(filepath), 'w')
        fcontentMaxMin.write(str(qtyCalculated) + '\t' + repr(minValues) + '\t' + repr(maxValues) )
        fcontentMaxMin.close()
    
    def reading_Max_min_file(self):
        fcontentMaxMin = open(self.filepathMaxMinCalculated, 'r')
        line = fcontentMaxMin.readline().replace('\n', '')
        data = line.split('\t')
        self.qtyDataCalculated = int(data[0])
        self.minValueCalculated = eval(data[1])
        self.maxValueCalculated = eval(data[2])
        fcontentMaxMin.close()
    
    def reading_calculateResult_normalized(self, filepath):
        results = []
        f = open(Formating.get_abs_file_path(filepath), 'r')
        firstLine = 0
        for line in f:
            if firstLine == 0:
                firstLine = 1
                continue
            cols = line.strip().replace('\n','').split(',')
            
            item_result = []
            item_result.append(cols[0])
            item_result.append(cols[1])
            scores = []
            for index_col in range(len(cols)-2):
                scores.append(eval(cols[2+index_col]))
            item_result.append(scores)  
            results.append(item_result)
        return results
    
    
    
    def executingCalculate(self):
        dataInicial = datetime.today()
        
        print "Starting Calculating Nodes not linked", dataInicial
        element = 0
        qtyofNodesToProcess = len(self.NodesNotLinked)
        qtyFeatures = len(self.preparedParameter.ScoresChoiced)
        results = []
        #for each node
        for nodenotLinked in self.NodesNotLinked:
            element = element+1
            Formating.printProgressofEvents(element, qtyofNodesToProcess, "Calculating features for nodes not liked: ")
            item_result = []
            for index_features in range(qtyFeatures):
                self.preparedParameter.ScoresChoiced[index_features][0].parameter = self.preparedParameter
                valueCalculated = self.preparedParameter.ScoresChoiced[index_features][0].execute(nodenotLinked[0],nodenotLinked[1]  )
                if valueCalculated < self.minValueCalculated[index_features]:
                    self.minValueCalculated[index_features] = valueCalculated
                if valueCalculated > self.maxValueCalculated[index_features]:
                    self.maxValueCalculated[index_features] = valueCalculated
                        
                item_result.append(valueCalculated)
                
            lineContent = []    
                #generating a vetor with the name of the feature and the result of the calculate
            for indice in range(qtyFeatures):
                lineContent.append(item_result[indice])
                    
                    
            results.append([nodenotLinked[0], nodenotLinked[1], lineContent ])
            
        print "Calculating Nodes not linked finished", dataInicial, datetime.today()
        self.qtyDataCalculated = len(results)
        return results    
    
    def __init__(self, preparedParameter, nodesNotLinked):
        
        self.preparedParameter = preparedParameter
        self.NodesNotLinked = nodesNotLinked
        self.minValueCalculated = list(99999 for x in self.preparedParameter.ScoresChoiced)
        self.maxValueCalculated = list(0 for x in self.preparedParameter.ScoresChoiced)
        self.qtyDataCalculated = 0
        
        
        
        