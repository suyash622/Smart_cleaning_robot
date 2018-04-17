import numpy as np
from matplotlib import pyplot as plt
import networkx as nx


class gen_path(object):
	def __init__(node_data,edge_data,special_edges):
		self.node_data=node_data
		self.edge_data=edge_data
		self.special_nodes=special_edges
		self.path=[]
		self.priority = []
		self.G=nx.Graph()


	def build_graph():
		for i in node_data:
			self.G.add_node(i)
		for e in edge_data:
			n1 = e[0]
			n2 = e[1]
			weight = e[3]
			self.G.add_edge(n1,n2)
			self.G[n1][n2]['weight'] = weight

	def Heurestics():
		for i in special_edges:
			self.priority.append(i)

	def master_path():

	def display_path():

	]

