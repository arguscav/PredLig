'''
Created on 8 de jul de 2015

@author: CarlosPM
'''
from featuring.AASFeature import AASFeature
from featuring.CNFeature import CNFeature
from featuring.JCFeature import JCFeature
from featuring.PAFeature import PAFeature
from formating.dblp.Formating import Formating
from featuring.TimeScore import TimeScore
from featuring.DomainTimeScore import DomainTimeScore
from featuring.DomainTimeScorevTwo import DomainTimeScorevTwo
from featuring.DomainJC import DomainJC

from featuring.WCNFeature import WCNFeature
from featuring.WAAFeature import WAAFeature
from featuring.AAWFeature import AAWFeature
from featuring.CNWFeature import CNWFeature
from featuring.PAWFeature import PAWFeature
from featuring.forweights.WeightTimeScore import WeightTimeScore
from featuring.forweights.WeightDomainScore import WeightDomainScore
from featuring.SPLFeature import SPLFeature
from featuring.LSFeature import LSFeature
from featuring.WSPLFeature import WSPLFeature
from featuring.DomainLS import DomainLS

class ParameterUtil(object):
    


    def __init__(self, parameter_file):
        parameterFile = Formating.get_abs_file_path(parameter_file)
        
        AllFeatures = []
        AllFeatures.append(AASFeature())
        AllFeatures.append(CNFeature())
        AllFeatures.append(JCFeature())
        AllFeatures.append(PAFeature())
        AllFeatures.append(TimeScore())
        #AllFeatures.append(LSFeature())
        
        AllFeatures.append(DomainTimeScore())
        AllFeatures.append(DomainJC())
        
        
        WeightedFeatures = []
        WeightedFeatures.append(WeightTimeScore())
        WeightedFeatures.append(WeightDomainScore())
        
        FeaturesForWeight = []
        FeaturesForWeight.append(WCNFeature())
        FeaturesForWeight.append(WAAFeature())
        FeaturesForWeight.append(CNWFeature())
        FeaturesForWeight.append(AAWFeature())
        FeaturesForWeight.append(PAWFeature())
        FeaturesForWeight.append(WSPLFeature())
                
        self.ScoresChoiced = []
        self.WeightsChoiced = []
        self.WeightedScoresChoiced = []
        
        
        with open(parameterFile) as f:
            lines = f.readlines()
            f.close()
        for line in lines:
            line = line.strip()
            line = line.replace('\n','')
            cols = line.split('\t')
            if cols[0] == 'linear_combination':
                self.linear_combination = eval(cols[1])
            if cols[0] == 'original_file':
                self.original_file = cols[1]
            if cols[0] == 'graph_file':
                self.graph_file = cols[1]
            if cols[0] == 'maxmincalculated_file':
                self.maxmincalculated_file = cols[1]
            if cols[0] == 'trainnig_graph_file':
                self.trainnig_graph_file = cols[1]
            if cols[0] == 'test_graph_file':
                self.test_graph_file = cols[1]
            if cols[0] == 'nodes_notlinked_file':
                self.nodes_notlinked_file = cols[1]
            if cols[0] == 'nodes_file':
                self.nodes_file = cols[1]
            if cols[0] == 'calculated_file':
                self.calculated_file = cols[1]
            if cols[0] == 'ordered_file':
                self.ordered_file = cols[1]
            if cols[0] == 'analysed_file':
                self.analysed_file = cols[1]
            if cols[0] == 'min_edges':
                self.min_edges = int(cols[1])
            if cols[0] == 'lengthVertex':
                self.lengthVertex = int(cols[1])
            if cols[0] == 'result_random_file':
                self.result_random_file = cols[1]
            if cols[0] == 't0':
                self.t0 = int(cols[1])
            if cols[0] == 't0_':
                self.t0_ = int(cols[1])
            if cols[0] == 't1':
                self.t1 = int(cols[1])
            if cols[0] == 't1_':
                self.t1_ = int(cols[1])
            if cols[0] == 'decay':
                self.decay = float(cols[1])
            if cols[0] == 'domain_decay':
                self.domain_decay = float(cols[1])
            if cols[0] == 'scores':
                features = cols[1].split(';')
                for feature in features:
                    #print feature
                    featureandweight = feature.split(':')
                    weight = float(featureandweight[1].split(',')[0])
                    orderingType = int(featureandweight[1].split(',')[1])
                    self.ScoresChoiced.append([AllFeatures[int(featureandweight[0])], weight, orderingType   ])
            
            if cols[0] == 'weights':
                features = cols[1].split(';')
                for feature in features:
                    featureandweight = feature.split(':')
                    self.WeightsChoiced.append([WeightedFeatures[int(featureandweight[0])], int(featureandweight[1])])
                
            if cols[0] == 'weighted_scores':
                features = cols[1].split(';')
                for feature in features:#0:1-1,0;
                    featureandweight = feature.split(':')
                    weight = featureandweight[1].split('-')[0]
                    weightfeatures = featureandweight[1].split('-')[1].split(',')[0]
                    orderingType = int(featureandweight[1].split('-')[1].split(',')[1])
                    item =  [FeaturesForWeight[int(featureandweight[0])], 
                                                       weight, 
                                                       weightfeatures, orderingType  ]
                    self.WeightedScoresChoiced.append(
                                                       item
                                                       )
                
        