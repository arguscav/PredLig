'''
Created on Oct 4, 2015

@author: cptullio
'''
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
import networkx
from featuring.FeatureBase import FeatureBase


if __name__ == '__main__':
    conjutodepalavrasA = set(['mae', '3333333'
                              ])
    conjutodepalavrasB = set(['mae', 'cachorro','2','3','4','5','7', '9'])
    f = (float)(len(conjutodepalavrasA.intersection(conjutodepalavrasB)))
    x = (float)(len(conjutodepalavrasA.union(conjutodepalavrasB)))
    if x == 0:
        print 0
    result =  f/x
    beta = 0.1;
    adicao = beta**result
    print "jc result: ", result, "final result: ", adicao
    numerador = 4.0
    denominador = 10.0
    print numerador / denominador
    print numerador / (denominador * adicao)