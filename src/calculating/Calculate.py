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
import mysql.connector



class Calculate(object):
    
    
    
        
    @staticmethod
    def reading_calculateLine(line):
        calcs = []
        cols = line.split('\t')
        for indice in range(len(cols) -2 ):
            calcs.append(float(line.split('\t')[indice].split(':')[1].replace('}','').strip()) )
        return [calcs, cols[len(cols)-2], cols[len(cols)-1]  ] 
    
    def normalize(self, data, indice):
        if self.maxValueCalculated[indice] == self.minValueCalculated[indice]:
            return data
        xnormalize = (data - self.minValueCalculated[indice])/(self.maxValueCalculated[indice] - self.minValueCalculated[indice])
        return xnormalize            
        
    def Separating_calculateFile(self):
        self.reading_Max_min_file()
        
        f =  open(self.filepathResult)
        fF = []
        for i in self.preparedParameter.ScoresChoiced:
            fF.append(open(self.filepathResult +  '.' +str(i) + '.txt', 'w'))
        element = 0
            
        for line in f:
            element = element + 1
            self.printProgressofEvents(element, self.qtyDataCalculated, "separating files: ")
                 
            calcs = []
            cols = line.split('\t')
            for indice in range(len(cols) -2 ):
                
                data = float(line.split('\t')[indice].split(':')[1].replace('}','').strip())
                xdata = self.normalize(data, indice)
                fF[indice].write( str(xdata) + ':' + cols[len(cols)-2]  + ':' +  cols[len(cols)-1] )
        f.close()
        for ffF in fF:
            ffF.close()
    
    def reading_Max_min_file(self):
        fcontentMaxMin = open(self.filepathMaxMinCalculated, 'r')
        line = fcontentMaxMin.readline().replace('\n', '')
        data = line.split('\t')
        self.qtyDataCalculated = int(data[0])
        self.minValueCalculated = eval(data[1])
        self.maxValueCalculated = eval(data[2])
        fcontentMaxMin.close()
    
    def getfilePathOrdered_separeted(self):
        data = []
        for indice in range(len(self.preparedParameter.ScoresChoiced)):
            data.append(self.filePathOrdered +  '.' +str(self.preparedParameter.ScoresChoiced[indice]) + '.txt')
        return data
    
    
    def generating_part_files_for_ordering_in_memory(self, file):
        total = self.qtyDataCalculated / 4
        if os.path.exists(file.name + '.part1.txt'):
            print "Separated Files already done.", datetime.today()
        else:
            fw1 = open(file.name + '.part1.txt', 'w')
            fw2 = open(file.name + '.part2.txt','w')
            fw3 = open(file.name + '.part3.txt','w')
            fw4 = open(file.name + '.part4.txt','w')
            element = 0
            for line in file:
                element = element+1
                if element < total:
                    fw1.write(line)
                elif element < (total*2):
                    fw2.write(line)
                elif element < (total*3):
                    fw3.write(line)
                else:
                    fw4.write(line)
            
            fw1.close()
            fw2.close()
            fw3.close()
            fw4.close()
        newfiles = [open(file.name + '.part1.txt', 'r'),open(file.name + '.part2.txt', 'r'),open(file.name + '.part3.txt', 'r'),open(file.name + '.part4.txt', 'r') ]
        return newfiles
        
    
    
        
    def Ordering_separating_File(self, topRank):
        print "Starting Ordering the Calculating  in Separating File", datetime.today()
        
        
        for indice in range(len(self.preparedParameter.ScoresChoiced)):
            print "Ordering feature: ", str(self.preparedParameter.ScoresChoiced[indice])
            fr = open(self.filepathResult +  '.' +str(self.preparedParameter.ScoresChoiced[indice]) + '.txt', 'r')
            print "Separating File Ordering feature: ", str(self.preparedParameter.ScoresChoiced[indice])
            filesPart = self.generating_part_files_for_ordering_in_memory(fr)
            fr.close()
            itemPart = 0
            for fp in filesPart:
                itemPart = itemPart+1
                fw = open(self.filePathOrdered +  '.' +str(self.preparedParameter.ScoresChoiced[indice]) + '.part'+ str(itemPart)+'.txt', 'w')
                print "Ordering " , fw.name
                data = []
                for line in fp:
                    cols = line.split(':')
                    data.append([float(cols[0]), cols[1], cols[2]])
                orderingByDesc = True
                if (self.preparedParameter.ScoresChoiced[indice][2] == 1):
                    orderingByDesc = False
                orderData = sorted(data, key=lambda value: value[0], reverse=orderingByDesc)
                data = None
                del data
                print "Saving data Ordering " , fw.name
                
                for item in orderData:
                    fw.write(str(item[0]) +'\t' + item[1] + '\t' + item[2] )
                orderData = None
                del orderData
                gc.collect()
                fw.close()
                fp.close()
            
            print "Now Ordering by top rank", datetime.now()
            FinalData = []
            for i in range(itemPart):
                frPart = open(self.filePathOrdered +  '.' +str(self.preparedParameter.ScoresChoiced[indice]) + '.part'+ str((i+1))+'.txt', 'r')
                element = 0
                for line in frPart:
                    element = element + 1
                    if element > topRank:
                        break
                    cols = line.split('\t')
                    FinalData.append([float(cols[0]), cols[1], cols[2]])
            orderingByDescFinal = True
            if (self.preparedParameter.ScoresChoiced[indice][2] == 1):
                orderingByDescFinal = False
            orderFinalData = sorted(FinalData, key=lambda value: value[0], reverse=orderingByDescFinal)
            fwFinal = open(self.filePathOrdered +  '.' +str(self.preparedParameter.ScoresChoiced[indice]) + '.txt', 'w')
            for item in orderFinalData:
                fwFinal.write(str(item[0]) +'\t' + item[1] + '\t' + item[2] )
             
            
            
            
        print "Ordering the Calculating  in Separating File FINISHED", datetime.today()
            


    def Ordering__using_memory_separating_File(self):
        print "Starting Ordering the Calculating  in Separating File", datetime.today()
        
        for indice in range(len(self.preparedParameter.ScoresChoiced)):
            
            fw = open(self.filePathOrdered +  '.' +str(self.preparedParameter.ScoresChoiced[indice]) + '.txt', 'w')
            
            fr = open(self.filepathResult +  '.' +str(self.preparedParameter.ScoresChoiced[indice]) + '.txt', 'r')
            print "reading file", str(self.preparedParameter.ScoresChoiced[indice])
            lines = fr.readlines()
            data = []
            element = 0
            qty = len(lines)
            for line in lines:
                element = element + 1
                if element % 2000 == 0:
                    self.printProgressofEvents(element, qty, "Buffering Calculations to ordering: ")
                
                cols = line.split(':')
                data.append([float(cols[0]), cols[1], cols[2]])
            del lines
            print "ordering file", str(self.preparedParameter.ScoresChoiced[indice])
            orderData = sorted(data, key=lambda value: value[0], reverse=True)
            element = 0
            for item in orderData:
                element = element + 1
                self.printProgressofEvents(element, self.qtyDataCalculated, "Saving Data Ordered: ")
                if element == 301:
                    break
                fw.write(str(item[0]) +'\t' + item[1] + '\t' + item[2] )
            fw.close()
            fr.close()
            del data
            del orderData
            print "Ordering the Calculating  in Separating File FINISHED", datetime.today()

    
    
    def printProgressofEvents(self, element, length, message):
        print message, str((float(element)/float(length))*float(100)) + '%', datetime.today()

    def printProgressofEventsWihoutPercent(self, element, length, message):
        print message, str(element) + ' of '  +  str(length) , datetime.today()

    
    def __init__(self, preparedParameter, filepathNodesNotLinked, filepathResult, filePathOrdered, filepathMaxMinCalculated):
        print "Starting Calculating Nodes not linked", datetime.today()
        
        self.preparedParameter = preparedParameter
        self.filePathOrdered = Formating.get_abs_file_path(filePathOrdered)
        self.filepathMaxMinCalculated = Formating.get_abs_file_path(filepathMaxMinCalculated)
        self.filepathResult = Formating.get_abs_file_path(filepathResult)
        self.filepathNodesNotLinked = Formating.get_abs_file_path(filepathNodesNotLinked)
        #for each links that is not linked all the calculates is done.
        element = 0
        qtyofResults = FormatingDataSets.getTotalLineNumbers(self.filepathNodesNotLinked)
        fcontentNodesNotLinked = open(self.filepathNodesNotLinked, 'r')
        if os.path.exists(self.filepathResult):
            print "Calculate already done for this file, please delete if you want a new one.", datetime.today()
            self.reading_Max_min_file()
            return
        
        fcontentCalcResult = open(self.filepathResult, 'w')
        
        self.minValueCalculated = list(99999 for x in self.preparedParameter.ScoresChoiced)
        self.maxValueCalculated = list(0 for x in self.preparedParameter.ScoresChoiced)
        
        qtyFeatures = len(self.preparedParameter.ScoresChoiced)
        qtyNodesCalculated = 0
        partialResults = []
        for lineofFile in fcontentNodesNotLinked:
            element = element+1
            item = VariableSelection.getItemFromLine(lineofFile)
            qtyothernodenotlinked = len(item[1])
            newelement = 0
            for neighbor_node in item[1]:
                newelement = newelement +1
                qtyNodesCalculated = qtyNodesCalculated + 1
                self.printProgressofEvents(element, qtyofResults, "Calculating features for nodes not liked: ")
                self.printProgressofEventsWihoutPercent(newelement, qtyothernodenotlinked, "Calculating nodes: " + str(item[0])  + ":" +  str(neighbor_node) )
            
                item_result = []
                #executing the calculation for each features chosen at parameter
                for index_features in range(qtyFeatures):
                    self.preparedParameter.ScoresChoiced[index_features][0].parameter = preparedParameter
                    valueCalculated = self.preparedParameter.ScoresChoiced[index_features][0].execute(item[0],neighbor_node) * self.preparedParameter.ScoresChoiced[index_features][1]
                    if valueCalculated < self.minValueCalculated[index_features]:
                        self.minValueCalculated[index_features] = valueCalculated
                    if valueCalculated > self.maxValueCalculated[index_features]:
                        self.maxValueCalculated[index_features] = valueCalculated
                        
                    item_result.append(valueCalculated)
                
                lineContent = []    
                #generating a vetor with the name of the feature and the result of the calculate
                for indice in range(qtyFeatures):
                    lineContent.append(str({str(self.preparedParameter.ScoresChoiced[indice]):item_result[indice]}) )
                partialResults.append([lineContent, item[0], neighbor_node])
                
            if element % 10 == 0:
                for item in partialResults:
                    for calc in item[0]:
                        fcontentCalcResult.write(calc + '\t')
                    fcontentCalcResult.write(str(item[1]) + '\t' + str(item[2])  + '\n'  )
                partialResults = []
        
        for item in partialResults:
            for calc in item[0]:
                fcontentCalcResult.write(calc + '\t')
            fcontentCalcResult.write(str(item[1]) + '\t' + str(item[2])  + '\n'  )
                
        
        fcontentCalcResult.flush()
        fcontentCalcResult.close()
        fcontentNodesNotLinked.close()
        fcontentMaxMin = open(self.filepathMaxMinCalculated, 'w')
        fcontentMaxMin.write(str(qtyNodesCalculated) + '\t' + repr(self.minValueCalculated) + '\t' + repr(self.maxValueCalculated) )
        fcontentMaxMin.close()
        print "Calculating Nodes not linked finished", datetime.today()
        
        