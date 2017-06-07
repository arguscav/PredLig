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

class ParallelClassifier:
	
	def __init__(self):
		pass
		
	def get_classifier_score(self, classifier, dataset, pair_class, fold, out_score, score_metric):
		trained_classifier = classifier.fit(dataset[fold[0]], pair_class[fold[0]])
		score = score_metric(pair_class[fold[1]], trained_classifier.predict(dataset[fold[1]]))
		out_score.put(score)
	
	def get_final_score(self, classifier, dataset, pair_class, folds, score_metric):
		out_q = multiprocessing.Queue()
		procs = []
		nprocs = len(folds)
			
		for fold in folds:
			p = multiprocessing.Process(target=self.get_classifier_score, args=(classifier, dataset, pair_class, fold, out_q, score_metric))
			procs.append(p)
			p.start()
				
		result = []
		for i in range(nprocs):
			result.append(out_q.get())
				
		for p in procs:
			p.join()
			
		score = sum(result)/len(result)
		
		return score
