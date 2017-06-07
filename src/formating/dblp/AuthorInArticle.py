'''
Created on 24 de jun de 2015

@author: CarlosPM
'''

class AuthorInArticle(object):
    
    def __init__(self, articleid, authorid):
        self.authorid = authorid
        self.articleid = articleid
        self.time = 0
