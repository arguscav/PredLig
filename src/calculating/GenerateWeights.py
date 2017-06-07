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



class GenerateWeigths(object):
    
    
    
    def __init__(self, preparedParameter, fileAllNodes):
        
        print "Starting Generating Weights for all Nodes", datetime.today()
        
        self.preparedParameter = preparedParameter
       
        self.filepathAllNodes = Formating.get_abs_file_path(fileAllNodes)
        
        self.preparedParameter.open_connection()
        self.preparedParameter.clean_database()
        
        fcontentAllNodes = open(self.filepathAllNodes, 'r')
        
        self.minValueCalculated = list(99999 for x in self.preparedParameter.WeightsChoiced)
        self.maxValueCalculated = list(0 for x in self.preparedParameter.WeightsChoiced)
        
        qtyFeatures = len(self.preparedParameter.WeightsChoiced)
        qtyNodesCalculated = 0
        
        for lineofFile in fcontentAllNodes:
            item = VariableSelection.getItemFromLine(lineofFile)
            item_result = []
            #executing the calculation for each features chosen at parameter
            for index_features in range(qtyFeatures):
                self.preparedParameter.WeightsChoiced[index_features][0].parameter = preparedParameter
                valueCalculated = self.preparedParameter.WeightsChoiced[index_features][0].execute(item[0],item[1]) * self.preparedParameter.WeightsChoiced[index_features][1]
                    
                if valueCalculated < self.minValueCalculated[index_features]:
                    self.minValueCalculated[index_features] = valueCalculated
                if valueCalculated > self.maxValueCalculated[index_features]:
                    self.maxValueCalculated[index_features] = valueCalculated
                        
                item_result.append(valueCalculated)
                
            self.preparedParameter.add_weight(item[0], item[1], item_result)
                
                
        
        self.preparedParameter.add_weight(-1,-1, qtyNodesCalculated)
        self.preparedParameter.add_weight(-2,-2, repr(self.minValueCalculated))
        self.preparedParameter.add_weight(-3,-3, repr(self.maxValueCalculated))
        self.preparedParameter.close_connection()
        print "Finishinig Generating Weights for all Nodes", datetime.today()
        
        