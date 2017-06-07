import numpy as np
import sklearn
import sys
import multiprocessing
from sklearn import svm
from sklearn import cross_validation
from sklearn import tree
from sklearn import neighbors
from sklearn import naive_bayes
from sklearn import ensemble
from classifier import ParallelClassifier

class LinkPrediction:
	"""
	A link predictor.
	This class builds a classifier model based on the classification dataset provider, and uses this model to predict the existence
	or absence of a link in a set of pairs of nodes.
	"""
	def __init__(self, dataset, folds_number, classifier = "CART", classifier_params = {"random_state": 10}, metric = "precision"):
		self.dataset = dataset
		self.classifier = classifier
		self.classifier_params = classifier_params
		self.metric = metric
		self.folds_number = folds_number
		self.classifiers = {
		 "CART": tree.DecisionTreeClassifier, 
		 "SVM": svm.SVC, 
		 "KNN": neighbors.KNeighborsClassifier, 
		 "NB": naive_bayes.GaussianNB, 
		 "RFC": ensemble.RandomForestClassifier
		 }
		self.metrics = {
			#"accuracy": sklearn.metrics.accuracy_score,
			"precision": sklearn.metrics.precision_score,
			"recall": sklearn.metrics.recall_score,
			"f1": sklearn.metrics.f1_score		  
		 }
		 
	def set_classifier(self, classifier):
		self.classifier = classifier
	
	def set_metric(self, metric):
		self.metric = metric
	
	def set_folds_number(self, folds_number):
		self.folds_number = folds_number
	
	def apply_classifier(self):
		parallel_classifier = ParallelClassifier()
		number_examples, number_attributes = self.dataset.shape
		examples = self.dataset[:,range(number_attributes-2)]
		examples_classes = self.dataset[:,[-2]]
		
		train_test_folds = []
		
		fold = np.zeros([number_examples])
		map_folds = {}
		
		for example in range(number_examples):
			fold[example] = self.dataset[example][-1]
			dict.setdefault(map_folds, fold[example], set())
			map_folds[fold[example]].add(example)
			
		for fold_examples in map_folds.values():
			train_test_folds.append((list(set(range(number_examples)) - fold_examples), list(fold_examples)))
		
		score = parallel_classifier.get_final_score(self.classifiers[self.classifier](**self.classifier_params), examples, examples_classes, train_test_folds, self.metrics[self.metric])
		return score
