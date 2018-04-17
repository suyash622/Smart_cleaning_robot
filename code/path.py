import numpy as np
from matplotlib import pyplot as plt
import netwrokX

class gen_path(object):
	def __init__(node_data,edge_data,special_nodes):
		self.node_data=node_data
		self.edge_data=edge_data
		self.special_nodes=special_nodes
		self.path=[]
		self.G=[]


	def 