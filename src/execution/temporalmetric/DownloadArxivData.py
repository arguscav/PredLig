'''
Created on Aug 22, 2015

@author: cptullio

First Step is the generation of the graph from the database informations.
We will need the file of parameter to indicate the place where the graph will be saved

'''
from formating.arxiv.Formating import Formating

def grqc(years):
    astroPh = Formating('/home/cmuniz/execMen/grafos/grqc_data')
    astroPh.subject = 'gr-qc'
    astroPh.yearstoRescue = years
    astroPh.readingOrginalDataset()


def hepph(years):
    astroPh = Formating('/home/cmuniz/execMen/grafos/hepph_data')
    astroPh.subject = 'hep-ph'
    astroPh.yearstoRescue = years
    astroPh.readingOrginalDataset()


def astroph(years):
    astroPh = Formating('/home/cmuniz/execMen/grafos/astroph_data')
    astroPh.subject = 'astro-ph'
    astroPh.yearstoRescue = years
    astroPh.readingOrginalDataset()


def condmat(years):
    astroPh = Formating('/home/cmuniz/execMen/grafos/condmat_data')
    astroPh.subject = 'cond-mat'
    astroPh.yearstoRescue = years
    astroPh.readingOrginalDataset()

def hepth(years):
    astroPh = Formating('/home/cmuniz/execMen/grafos/hepth_data')
    astroPh.subject = 'hep-th'
    astroPh.yearstoRescue = years
    astroPh.readingOrginalDataset()


if __name__ == '__main__':
    #hepth([2000,2001,2002,2003,2004,2005])    
    hepph([1994,1995,1996,1997,1998,1999])    
    #condmat([2000,2001,2002,2003,2004,2005])    
    #astroph([2000,2001,2002,2003,2004,2005])    
    #grqc([2000,2001,2002,2003,2004,2005])    
    
