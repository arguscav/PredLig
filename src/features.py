import networkx as nx
from networkx.algorithms import bipartite
import numpy as np
import inspect
import random

class FeatureConstructor:
	"""
	A feature constructor.
	
	This class calculates topological attributes for a defined pair of vertices, based on the structure of the provided graph.
	"""
	def __init__(self, graph, node_1=None, node_2=None):
		self.graph = graph
		self.node_1 = node_1
		self.node_2 = node_2
		self.clustering_dict = nx.clustering(graph)
		self.betweenness_dict = nx.betweenness_centrality(graph)
		self.average_neighbor_degree_dict = nx.average_neighbor_degree(graph)
		
		self.attributes_map = {
			"adamic_adar_similarity": self.adamic_adar_similarity,	
			"average_clustering_coefficient": self.average_clustering_coefficient,	
			"average_neighbor_degree_sum": self.average_neighbor_degree_sum,	
			"betweenness_centrality": self.betweenness_centrality,	
			"closeness_centrality_sum": self.closeness_centrality_sum,	
			"clustering_coefficient_sum": self.clustering_coefficient_sum,	
			"common_neighbors": self.common_neighbors,	
			"cosine": self.cosine,	
			"jaccard_coefficient": self.jaccard_coefficient,	
			"katz_measure": self.katz_measure,	
			"preferential_attachment": self.preferential_attachment,		
			"square_clustering_coefficient_sum": self.square_clustering_coefficient_sum,	
			"sum_of_neighbors": self.sum_of_neighbors,	
			"sum_of_papers": self.sum_of_papers,
			"get_shortest_path_length": self.get_shortest_path_length,
			"get_second_shortest_path_length": self.get_second_shortest_path_length				
		}
		
		if(self.node_1 != None and self.node_2 != None):
			self.neighbors_1 = self.all_neighbors(self.node_1)
			self.neighbors_2 = self.all_neighbors(self.node_2)
	
	def set_nodes(self, node_1, node_2):
		self.node_1 = node_1
		self.node_2 = node_2
		self.neighbors_1 = self.all_neighbors(self.node_1)
		self.neighbors_2 = self.all_neighbors(self.node_2)
		
	def all_neighbors(self, node):
		neighbors = set()
		for neighbor in list(nx.all_neighbors(self.graph, node)):
			neighbors.add(neighbor)
		return neighbors - set([node])

	def common_neighbors(self):
		return len(self.neighbors_1.intersection(self.neighbors_2))

	def sum_of_neighbors(self):
		return len(self.neighbors_1) + len(self.neighbors_2)
		
	def jaccard_coefficient (self):
		return len(self.neighbors_1.intersection(self.neighbors_2))/len(self.neighbors_1.union(self.neighbors_2))

	def adamic_adar_similarity(self):
		measure = 0
		for neighbor in self.neighbors_1.intersection(self.neighbors_2):
			secondary_neighbors = self.all_neighbors(neighbor)
			measure += 1 / (np.log10(len(secondary_neighbors)))
		
		return measure
		
	def preferential_attachment(self):
		return len(self.neighbors_1) * len(self.neighbors_2)
		
	def katz_measure(self, beta, min_length):
		measure = 0
		if nx.shortest_path_length(self.graph, self.node_1, self.node_2) >= min_length:
			for i in nx.all_simple_paths(self.graph, self.node_1, self.node_2, min_length):
				measure += beta**len(i) * len(i)
		return measure

	def cosine(self):
		return self.common_neighbors() / self.preferential_attachment()

	def all_papers(self, graph, author):
		years = set()
		papers = 0
		for paper in list(nx.all_neighbors(graph, author)):
			years.add(graph.node[paper]['year'])
			papers += 1
		
		return papers/len(years)

	def sum_of_papers(self, graph, node_1, node_2):
		papers_1 = self.all_papers(graph, node_1)
		papers_2 = self.all_papers(graph, node_2)
		
		return papers_1 + papers_2
	
	def clustering_coefficient_sum(self):
		return self.clustering_dict[self.node_1] + self.clustering_dict[self.node_2]
	
	def betweenness_centrality(self):
		return self.betweenness_dict[self.node_1] * self.betweenness_dict[self.node_2]
		
	def closeness_centrality_sum(self):
		return nx.closeness_centrality(self.graph, self.node_1) + nx.closeness_centrality(self.graph, self.node_2)
	
	def average_neighbor_degree_sum(self):
		return self.average_neighbor_degree_dict[self.node_1] + self.average_neighbor_degree_dict[self.node_2]
	
	def average_clustering_coefficient(self):
		return nx.average_clustering(self.graph, [self.node_1, self.node_2])
	
	def square_clustering_coefficient_sum(self):
		return nx.square_clustering(self.graph, [self.node_1])[self.node_1] + nx.square_clustering(Gt, [self.node_2])[self.node_2]
	
	def get_shortest_path_length(self):
		return nx.shortest_path_length(self.graph, source=self.node_1, target=self.node_2)
	
	def get_second_shortest_path_length(self):
		shortest_paths_edges = []
		second_shortest_path_length = -1
		for path in nx.all_shortest_paths(self.graph, source=self.node_1, target=self.node_2):
			path_edges = self.get_edges_from_path(path)
			shortest_paths_edges.append(path_edges)
			self.graph.remove_edges_from(path_edges)
		
		second_shortest_path_length = nx.shortest_path_length(self.graph, self.node_1, self.node_2)
		for path in shortest_paths_edges:
			self.graph.add_edges_from(path)
		
		return second_shortest_path_length
	
	def get_edges_from_path(self, path):
		return [(path[node], path[node+1]) for node in range(len(path) -1)]
