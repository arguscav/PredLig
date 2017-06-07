'''
Created on Aug 22, 2015

@author: cptullio

First Step is the generation of the graph from the database informations.
We will need the file of parameter to indicate the place where the graph will be saved

'''
from parametering.ParameterUtil import ParameterUtil

from formating.arxiv.Formating import Formating

def grqc(years):
    astroPh = Formating('/grafos/grqc_data')
    astroPh.subject = 'gr-qc'
    astroPh.yearstoRescue = years
    astroPh.readingOrginalDataset()


def hepph(years):
    astroPh = Formating('/grafos/hepph_data')
    astroPh.subject = 'hep-ph'
    astroPh.yearstoRescue = years
    astroPh.readingOrginalDataset()


def astroph(years):
    astroPh = Formating('/grafos/astroph_data')
    astroPh.subject = 'astro-ph'
    astroPh.yearstoRescue = years
    astroPh.readingOrginalDataset()


def condmat(years):
    astroPh = Formating('/grafos/condmat_data')
    astroPh.subject = 'cond-mat'
    astroPh.yearstoRescue = years
    astroPh.readingOrginalDataset()

def hepth(years):
    astroPh = Formating('/grafos/hepth_data')
    astroPh.subject = 'hep-th'
    astroPh.yearstoRescue = years
    astroPh.readingOrginalDataset()


if __name__ == '__main__':
    hepph([[2010,2011,2012,2013,2014,2015]])    
    grqc([[2010,2011,2012,2013,2014,2015]])    
    hepph([[2010,2011,2012,2013,2014,2015]])    
    condmat([[2010,2011,2012,2013,2014,2015]])    
    astroph([[2010,2011,2012,2013,2014,2015]])    
    
