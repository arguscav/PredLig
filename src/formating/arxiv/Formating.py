'''
Created on Aug 23, 2015

@author: cptullio
'''
from formating.FormatingDataSets import FormatingDataSets
import urllib
import xml.dom.minidom
import time
import feedparser
import networkx
import gc
from datetime import datetime
import hashlib
import unicodedata
    
class Formating(FormatingDataSets):
    '''
    classdocs
    '''
    
    def __init__(self, graphfile):
    
        super(Formating, self).__init__('',graphfile)
        self.subject = 'astro-ph'
        self.yearstoRescue = [2009,2010,2011,2012,2013,2014]
        
    def get_qty_records_mid_year(self,year):
        url = 'http://export.arxiv.org/api/query?search_query=cat:'+ self.subject+'*+AND+submittedDate:[' +str(year) + '01010000+TO+' +str(year)+ '06312359]&start=0&max_results=1'
        data = urllib.urlopen(url).read()
        xmldoc = xml.dom.minidom.parseString(data)
        qtyRecordsMid = int(xmldoc.getElementsByTagName('opensearch:totalResults')[0].childNodes[0].data)
        time.sleep(3)
        url = 'http://export.arxiv.org/api/query?search_query=cat:'+ self.subject+'*+AND+submittedDate:[' +str(year) + '07010000+TO+' +str(year)+ '12312359]&start=0&max_results=1'
        data = urllib.urlopen(url).read()
        xmldoc = xml.dom.minidom.parseString(data)
        qtyRecordsMidFinal = int(xmldoc.getElementsByTagName('opensearch:totalResults')[0].childNodes[0].data)
        time.sleep(3)
        return [qtyRecordsMid,qtyRecordsMidFinal]

    def converter(self, dado):
        texto = dado.replace('.', '')
        texto = texto.replace('-', '')
        texto = texto.replace('\'' , '')
        texto = texto.replace(',' , '')
        texto = texto.replace('~', '')
        texto = texto.replace('{', '')
        texto = texto.replace('}', '')
        texto = texto.replace('}', '')
        texto = texto.replace('/', '')
        texto = texto.replace('\\', '')
        texto = texto.replace('"', '')
        return texto.strip()
     
    def get_articles(self,search_query, start, total_results,results_per_iteration):
        base_url = 'http://export.arxiv.org/api/query?'
        new_article = []
        inicio = start
        for i in range(inicio,total_results,results_per_iteration):
            print "Results %i - %i" % (i,i+results_per_iteration)
    
            query = 'search_query=%s&start=%i&max_results=%i' % (search_query,i,results_per_iteration)
            
            response = urllib.urlopen(base_url+query).read()
            print 'Parsing response'
            feed = feedparser.parse(response)
            
            papers = feed.entries
            print (base_url+query), 'results: ', len(papers)
        
            for entry in papers:
                idpaper = str('%s' % entry.id.split('/abs/')[-1])
                title = str(entry.title.encode("utf-8").strip().replace('\n', ''))
                yearPublication = int(entry.published.split('-')[0])
                authors = set()
                categories = set()
                for t in entry.tags:
                    categories.add(t.term.replace('\n', ''))
                
                
                for a  in entry.authors:
                    authorname = a.name.replace('\n', '')
                    authors.add( self.converter(str.upper(unicodedata.normalize('NFKD', authorname).encode('ascii','ignore') ) ) )
                
                data = [idpaper, title,  yearPublication, categories, authors ] 
                new_article.append(data)
               
      
            # Remember to play nice and sleep a bit before you call
            # the api again!
            print 'Sleeping for 10 seconds' 
            time.sleep(10)
        return new_article

    
    def generating_graph(self):
        
        self.Graph = networkx.MultiGraph()
        #_u = lambda t: t.decode('UTF-8', 'replace') if isinstance(t, str) else t
        authors = set()
        papers = set()
        
        total_papers = 0
        begin = datetime.today()
        for year in  self.yearstoRescue:
            f = open(self.get_abs_file_path(self.GraphFile) + '.' +str(year) + '.txt', 'r')
            print 'reading', f.name
            y = 0
            for line in f:
                
                cols = line.split('\t')
                if len(cols) == 5:
                    
                    keywords_not_clean = eval(cols[3])
                    keywords = set()
                    for k in keywords_not_clean:
                        keywords.add(k)
                    papers.add(str(cols[0]))
                    myAresta = {'id_edge': str(cols[0]), 'title': cols[1].decode("latin_1"), 'time' : int(cols[2]), 'keywords': repr(keywords)}
                    
                    myVertices = sorted(eval(cols[4]))
                    for v in myVertices:
                        authors.add(hashlib.md5(v).hexdigest())
                    
                    if (len(myVertices) == 1):
                        self.Graph.add_edge(hashlib.md5(myVertices[0]).hexdigest(),hashlib.md5(myVertices[0]).hexdigest(),  attr_dict=myAresta)
                        
                    else:
                    
                        for vertice in myVertices:
                            otherVertices =  set(n for n in myVertices if n > vertice)
                            for otherVertice in otherVertices:
                                try:
                                    self.Graph.add_edge(hashlib.md5(vertice).hexdigest(),hashlib.md5(otherVertice).hexdigest(), attr_dict=myAresta)
                                except Exception as inst:
                                    raise Exception(vertice + ", "  + otherVertice)
                    
                else:
                    y = y +1
            print 'total of articles not imported: ', y
            f.close()
        print 'TOTAL DE PAPERS:', len(papers)
        print 'TOTAL DE AUTORES:', len(authors)
        #print sorted(papers)
        #print authors
                    
                        
                
           
            
         
    
    def readingOrginalDataset(self):
        #yearstoRescue = [2005,]
        #yearstoRescue = [2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014]
        #yearstoRescue = [1994,1995,1996,1997,1998,1999]
        
        for year in  self.yearstoRescue:
            articles = []
            qty = self.get_qty_records_mid_year(year);
            print qty
            search_queryMid = 'cat:'+ self.subject+'*+AND+submittedDate:['+str(year)+'01010000+TO+'+str(year)+'06312359]' # search for electron in all fields
            search_queryfinal = 'cat:'+ self.subject+'*+AND+submittedDate:['+str(year)+'07010000+TO+'+str(year)+'12312359]' # search for electron in all fields
            print "getting Begin"
            begin = None
            element = 0
            while True:
                element = element+1
                begin = self.get_articles(search_queryMid, 0, qty[0], 2000)
                if len(begin) == qty[0]:
                    break
                else:
                    print 'Did not get everything... trying again...', element, len(begin)
                if element == 10:
                    print 'Did not work exit everything'
                    exit()
            
            for i in begin:
                articles.append(i)
            print "getting Final"
            final = None
            element = 0
            while True:
                final = self.get_articles(search_queryfinal, 0, qty[1], 2000)
                if len(final) == qty[1]:
                    break
                else:
                    print 'Did not get everything... trying again...', element, len(final)
                if element == 10:
                    print 'Did not work exit everything'
                    exit()
            for j in final:
                articles.append(j)
            
            f = open(self.get_abs_file_path(self.GraphFile) + '.' +str(year) + '.txt', 'w')
            for item in articles:
                f.write(item[0] + '\t' + item[1] + '\t' + str(item[2]) + '\t' + repr(item[3] ) + '\t'+ repr(item[4]) + '\n')
            f.close()
            articles = None
            del articles
        #self.generating_graph()    
                
                
        
        
        
                
            
    