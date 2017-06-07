'''
Created on 24 de jun de 2015

@author: CarlosPM
'''
from formating.FormatingDataSets import FormatingDataSets
from formating.dblp.Article import Article
from formating.dblp.Author import Author
from formating.dblp.AuthorInArticle import AuthorInArticle
import networkx
from datetime import datetime

class Formating(FormatingDataSets):
	
	def readingOrginalDataset(self):
		print "Starting Reading Original Dataset", datetime.today()
		with open(self.OriginalDataSet) as f:
			self.OrignalContent = f.readlines()
			f.close()
		
		articleid = 0
		articles = []
		authornames = []
		authorofArticles = []
		authors = []
		article = None
		element = 0
		for line in self.OrignalContent:
			element = element+1
			FormatingDataSets.printProgressofEvents(element, len(self.OrignalContent), "Reading File Content to Generate Graph: ")
			line = line.strip()
			if line.startswith('#*'):
				articleid = articleid+1
				article = Article('p_' + str(articleid))
				article.articlename = line.replace('#*','').replace('\r\n','')
			if line.startswith('#t'):
				article.time = line.replace('#t','').replace('\r\n','')
			
			if line.startswith('#@'):
				authorsofArticle = line.replace('#@','').replace('\r\n','').split(',')
				for author in authorsofArticle:
					author = author.strip()
					if not author in authornames:
						authornames.append(author)
					articleauthor = AuthorInArticle(article.articleid, authornames.index(author)+1)
					authorofArticles.append(articleauthor)
			if line.startswith('#!'):
				articles.append(article)
		for index in range(len(authornames)):
			author = Author(index+1, authornames[index])
			authors.append(author)
		self.Graph = networkx.Graph()
		for item_article in articles:
			self.Graph.add_node(item_article.articleid, {'node_type' : 'E', 'title' : item_article.articlename.decode("latin_1"), 'time' : int(item_article.time) })
		for item_author in authors:
			self.Graph.add_node(int(item_author.authorid), {'node_type' : 'N', 'name' : item_author.name.decode("latin_1") })
		for item_edge in authorofArticles:
			self.Graph.add_edge(item_edge.articleid, int(item_edge.authorid) )
		
		print "Reading Original Dataset finished", datetime.today()
		
		
	
	
					

	def __init__(self, filepathOriginalDataSet, graphfile):
	
		super(Formating, self).__init__(filepathOriginalDataSet,graphfile)
	
			
			
		