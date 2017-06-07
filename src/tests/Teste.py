'''
Created on 11 de mar de 2016

@author: Administrador
'''
import numpy as np
from sklearn.metrics import roc_auc_score

if __name__ == '__main__':
    y_true = np.array([1, 0, 0, 0, 0, 0, 1, 0, 0, 0])
    #y_scores = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    y_scores = None #np.array([0.2, 0.8, 0.8, 0.8, 0.8, 0.8, 0.2, 0.8, 0.8, 0.8])
    print roc_auc_score(y_true)