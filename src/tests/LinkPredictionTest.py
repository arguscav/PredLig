'''
Created on Jun 1, 2015

@author: cptullio
'''
import unittest

from sample import Sample
from linkprediction import LinkPrediction
from datetime import datetime

class Test(unittest.TestCase):


   def test_amazon_resume(self):
        print datetime.now()
        print "Instantiating Sample"
        sample = Sample("/Users/cptullio/Predicao-de-Links/PredLig/src/data/amazon_resume.txt", 20, (0.5, 0.5))
        print datetime.now()
        print "Configuring Attributes or Features"
        sample.set_attributes_list({"preferential_attachment":{}, "common_neighbors":{}, "sum_of_neighbors":{}})
        print datetime.now()
        print "Rescue the Sample"
        sample.get_sample()
        print datetime.now()
        print "Classifying the data"
        table = sample.set_classification_dataset()
        print datetime.now()
        print "Making Prediction Link"
        predictor = LinkPrediction(dataset = table, folds_number = 2)
        print datetime.now()
        print "Applying Classifier"
        print predictor.apply_classifier()
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()