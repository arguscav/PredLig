import networkx as nx 
from networkx.algorithms import bipartite 
import random 
import numpy as np
import sys
import sklearn
import features
import linkprediction

class Sample:
	"""
	A sample extractor.
	
	This class extracts a sample of pairs of vertices from the graph that represents the original data, according to the defined parameters.
	It can be used for both future and missing link prediction tasks, represented as 0 or 1 in the 'task' variable, respectively.
	"""
	def __init__(self, dataset, sample_size, sample_proportions, task = 1, future_dataset = None, k_fold = 2):
		self.dataset = dataset
		self.future_dataset = future_dataset
		self.sample_size = sample_size
		self.positive_examples_size = sample_proportions[0]
		self.negative_examples_size = sample_proportions[1]
		self.edges = set()
		self.positive_examples = set()
		self.negative_examples = set()
		self.original_graph = None
		self.graph_training = None
		self.graph_test = None
		self.task = task
		self.attributes_list = {}
		self.k_fold = k_fold
		self.classification_dataset = None
	
	def set_attributes_list(self, attributes_list):
		self.attributes_list = attributes_list
		self.ordered_attributes_list = sorted(self.attributes_list.keys())
		
	def get_future_link_graph(self):
		Graph = nx.graph()
		for line in self.future_dataset.readlines():
			line = line.strip()
			col = line.split(';')
			node1_id = int(col[0])
			node2_id = "p%s" %(int(col[1]))
			Graph.add_edge(node1_id, node2_id)
		return Graph
		
	def set_test_graph(self, graph_test):
		self.graph_test = graph_test
	
	def is_sublist(self, mlist, sublist):
		return ",".join(map(str, sublist)) in ",".join(map(str, mlist))
		
	def nodes_in_path(self, paths, first_node, second_node):
		""" 
		Verifies if a pair of nodes is part of some set of paths
		"""
		for path in paths:
			if self.is_sublist(path, [first_node, second_node]) or self.is_sublist(path, [second_node, first_node]):
				return True
		return False
	
	def get_pair_of_neighbors_nodes(self, Graph):
		return random.sample(Graph.edges(), 1)[0]
	
	def get_total_edges(self):
		return self.positive_examples.union(self.negative_examples)
	
	def get_missing_link_positive_pair_of_nodes(self, paths):
		while True:
			first_node, second_node = self.get_pair_of_neighbors_nodes(self.graph_training)
			if self.nodes_in_path(paths, first_node, second_node) or (first_node, second_node) in self.positive_examples:
				continue
				
			self.graph_training.remove_edge(first_node, second_node)
			if not nx.has_path(self.graph_training, first_node, second_node):
				self.graph_training.add_edge(first_node, second_node)
				continue
			
			return (first_node, second_node)
	
	def get_future_link_positive_pair_of_nodes(self, paths):
		while True:
			first_node, second_node = random.sample(self.graph_test.edges(), 1)[0]
			if self.graph_training.has_edge(first_node, second_node) or (first_node, second_node) in self.positive_examples:
				continue
			return (first_node, second_node)
			
	
	def get_positive_examples(self):
		"""
		Extracts the pairs of nodes of the positive class from the graph. Those pairs of nodes have link(s) between them in the missing
		link prediction, or have link(s) in the future period of time in the future link prediction.
		"""
		paths = set()
		get_pair_of_nodes = self.get_future_link_positive_pair_of_nodes if self.task == 0 else self.get_missing_link_positive_pair_of_nodes
		while len(self.positive_examples) < (self.sample_size * self.positive_examples_size):
			edge = get_pair_of_nodes(paths)
			if edge not in self.positive_examples:
				paths.add(tuple(nx.shortest_path(self.graph_training, edge[0], edge[1])))
				self.positive_examples.add(edge)
	
	def get_missing_link_negative_pair_of_nodes(self):
		while True:
			first_node, second_node = random.sample(self.graph_training.nodes(), 2)
			if not self.graph_training.has_edge(first_node, second_node) and not ((first_node, second_node) in self.negative_examples):
				return (first_node, second_node)
	
	def get_future_link_negative_pair_of_nodes(self):
		while True:
			first_node, second_node = self.get_missing_link_negative_pair_of_nodes()
			if not self.graph_test.has_edge(first_node, second_node):
				return (first_node, second_node)
	
	def get_negative_examples(self):
		"""
		Extracts the pairs of nodes of the negative class from the graph. Those pairs of nodes have no link between them in the missing
		link prediction, or have no link in the future period of time in the future link prediction.
		"""
		get_pair_of_nodes = self.get_future_link_negative_pair_of_nodes if self.task == 0 else self.get_missing_link_negative_pair_of_nodes
		while len(self.negative_examples) < (self.sample_size * self.negative_examples_size):
			self.negative_examples.add(get_pair_of_nodes())
			
	def get_sample(self):
		"""
		Extracts the whole sample from the graph representing the original dataset. 
		"""
		Graph = nx.Graph()
		dataset = open(self.dataset)
		for line in dataset.readlines():
			line = line.strip()
			col = line.split(';')
			iid = int(col[0])
			Graph.add_node(iid, {'bipartite': 0})
			pid = "p%s" %(int(col[1]))
			Graph.add_node(pid, {'bipartite': 1})
			Graph.add_edge(iid, pid)
		
		dataset.close()
		
		self.original_graph = Graph.copy()

		nodes = set(n for n,d in Graph.nodes(data=True) if d['bipartite'] == 1)
		
		Gt = nx.Graph()
		for node in nodes:
			for intermediate_node in list(nx.all_neighbors(Graph, node)):
				for second_node in list(nx.all_neighbors(Graph, intermediate_node)):
					Gt.add_edge(node, second_node)
		
		self.graph_training = Gt.copy()
		self.graph_test = Gt.copy() if self.task == 1 else self.get_future_links_graph()
		
		self.get_positive_examples()
		self.get_negative_examples()
	
	def set_dataset_folds(self):
		"""
		Defines the correspondent folds for each example of the sample.
		"""
		number_lines = len(self.classification_dataset)
		number_examples = range(0, number_lines)
		fold_half_size = (number_lines/self.k_fold)/2
		for fold in range(self.k_fold):
			for counter in range(fold_half_size):
				for class_type in range(0, 2):
					while True:
						example = random.sample(number_examples, 1)[0]
						if self.classification_dataset[example][-2] == class_type:
							self.classification_dataset[example][-1] = fold
							number_examples.remove(example)
							break
	
	def normalize_attributes(self):
		"""
		Normalizes the values of the attributes by extracting the mean of the attribute and dividing the result by the standard deviation. 
		"""
		attributes_number = self.classification_dataset.shape[1] - 2
		examples = range(self.classification_dataset.shape[0])
		for attribute in range(attributes_number):
			std = np.std(self.classification_dataset[[examples],[attribute]])
			if std == 0:
				self.classification_dataset[[examples],[attribute]] = 0
			else:
				self.classification_dataset[[examples],[attribute]] = (self.classification_dataset[[examples],[attribute]] - self.classification_dataset[[examples],[attribute]].mean())/np.std(self.classification_dataset[[examples],[attribute]])
		
	def set_classification_dataset(self):
		"""
		Calculates the attributes for each example of the sample, and returns it as a matrix ready for applying the classification
		algorithms, in order to perform the link prediction.
		"""
		self.classification_dataset = np.zeros((self.sample_size, len(self.attributes_list) + 2))
		line = 0
		attributes_calculator = features.FeatureConstructor(self.graph_training)
		for edge in self.positive_examples.union(self.negative_examples):
			first_node, second_node = edge
			attributes_calculator.set_nodes(first_node, second_node)
			pair_class = 0 if edge in self.negative_examples else 1
			column = 0
			for function in self.ordered_attributes_list:
				parameters = self.attributes_list[function]
				self.classification_dataset[line][column] = attributes_calculator.attributes_map[function](**parameters)
				column += 1
			self.classification_dataset[line][-2] = pair_class
			line += 1
		
		self.normalize_attributes()
		self.set_dataset_folds()
		return self.classification_dataset
		
		
if __name__ == "__main__":
	sample = Sample("/Users/cptullio/git/Predicao-de-Links/PredLig/src/formating/data/amazon_al.txt", 20, (0.5, 0.5))
	sample.set_attributes_list({"preferential_attachment":{}, "common_neighbors":{}, "sum_of_neighbors":{}})
	sample.get_sample()
	table = sample.set_classification_dataset()
	predictor = linkprediction.LinkPrediction(dataset = table, folds_number = 2)
	print predictor.apply_classifier()
	
