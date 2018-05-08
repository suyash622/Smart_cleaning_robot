
import os
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
import sys
import argparse
import plotly
import time
class gen_path(object):
	def __init__(self,node_data,nodes,origin,target,threshold):  ## node_data = [x,y] #edge_data = distance 
		self.node_data=node_data
		self.nodes = nodes
		self.ball_node = []
		self.path=[]
		self.origin = origin
		self.target = target 
		self.threshold = threshold   

		self.G=nx.Graph()

	def build_graph(self):
		for i in range(0,self.nodes):  
			if (self.node_data[i][3]=='b'):
				self.ball_node.append(self.node_data[i])        
				self.G.add_node(self.node_data[i])

		# self.G.add_edge(self.origin,self.node_data[0])
		for i in range(0,len(self.ball_node)-1):
			self.G.add_edge(self.ball_node[i],self.ball_node[i+1])
		for i in range(0,len(self.ball_node)-1):
			for i in range(i,len(self.ball_node)-1):
				self.G[self.ball_node[i]][self.ball_node[i+1]]['weight'] = self.weight_calculate(self.ball_node[i],self.ball_node[i+1])

		# self.G.add_edge(self.node_data[i],self.target)

	def weight_calculate(self,n1,n2):
		return (n1[0]-n2[0])**2 + (n1[1]-n2[1])**2

	def master_path(self):  
		self.path =nx.dijkstra_path(self.G,source=self.ball_node[0],target=self.ball_node[-1])

		self.path = list(self.path)
		self.path.insert(0,self.origin)
		self.path.append(self.target)
		for i in range(0,len(self.path)-1):
			x_off,y_off,done = self.isobstacle(list(self.path[i]),list(self.path[i+1]))
			if done:
				print i
				self.modify_path(i,x_off,y_off)
				done = False
	

	def modify_path(self,pos,x,y):
		self.path.insert(pos+1,[x,y,0.0,'new_way'])

	def isobstacle(self,p1,p2):
		p1 = np.array(p1[:2])
		p2 = np.array(p2[:2])
		

		for i,p3 in enumerate(self.node_data):
			# print p3
			print i
			if(p3[3]=='c'or p3[3]=='j'):
				p3 = np.array(list(p3[:2]))
				# print p1,p2,p3
				# print p2-p1,p3-p1
				# exit()
				# d = np.cross(p2-p1,p1-p3)
				# print d
				# exit()
				d = np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)
				
				if (d < self.threshold):
					x4 = p3[0] - (self.threshold-d)* (p1[1]-p2[1])
					y4 =  p3[1] + (self.threshold-d) * (p1[0]-p2[0])

					return x4,y4,True

		return 0,0,False
			
	def return_path(self):
		return self.path

	def display_path(self):
		x =[]
		y =[]
		for i in self.path:
			x.append(i[0])
			y.append(i[1])
		plt.plot(x,y,'-ro')
		plt.gca().set_aspect('equal', adjustable='box')
		plt.show()

	def animate(self):
		x =[]
		y =[]
		intervals = 1
		print self.path
		for i in range(0,len(self.path)):

			x_t,y_t = self.path[i][0],self.path[i][1]
			x.append(x_t)
			y.append(y_t)

		
		N = len(x)
		data=[dict(x=x, y=y, 
		   mode='lines', 
		   line=dict(width=2, color='blue')
		  ),
		 dict(x=x, y=y, 
		   mode='lines', 
		   line=dict(width=2, color='blue')
		  ),
		 dict(x=x, y=y, 
		   mode='lines', 
		   line=dict(width=2, color='blue')
		  )
		]

		xm = np.min(np.array(x)) - 2
		xM = np.max(np.array(x)) + 2
		ym = np.min(np.array(x)) - 2
		yM = np.max(np.array(y)) + 2


		layout=dict(xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
			yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
			title='Path of the Cleaning robot', hovermode='closest',
			updatemenus= [{'type': 'buttons',
						   'buttons': [{'label': 'Play',
										'method': 'animate',
										'args': [None]}]}])


		frames=[dict(data=[dict(x=[self.node_data[i][0] for i in range(self.nodes)], 
						y=[self.node_data[i][1] for i in range(self.nodes)], 
						mode='markers', 
						name = 'All obstacles',
						marker=dict(color='red', size=5)
						),
						dict(x=[self.path[i][0] for i in range(0,len(self.path))], 
						y=[self.path[i][1] for i in range(0,len(self.path))], 
						mode='line', 
						name= 'Traversable Obstacles ',
						marker=dict(color='green', size=7),
						),
				 		dict(x=[x[k]], 
						y=[y[k]], 
						mode='markers', 
						name = 'Path',
						marker=dict(color='blue', size=12)
						)] ) for k in range(N)]    


		figure1=dict(data=data, layout=layout, frames=frames)          
		plotly.offline.plot(figure1)

	def generate_points(self,p1,p2,n):
		x_t=[] 
		y_t=[]
		for i in range(n):
			 x_t.append(self.lerp(p1[0],p2[0],1./n*i))
			 y_t.append(self.lerp(p1[1],p2[1],1./n*i))
		return x_t,y_t
	def lerp(self,v0, v1, i):
		return (v0 + i * (v1 - v0))
def readFile(path):
	return open(path, 'rt')

def main(args):


	args = parser_arguments()
	display = args.display
	animate = args.animate
	file = args.fil
	inputFile = readFile(file)
	inputString = inputFile.read()
	pdata = dict()
	node_id =0
	x = []
	y = []
	z = []
	node_type =[]

	for line in inputString.splitlines():
		
		if line[0][0].isalpha() == False:
			line = line.split(' ')
			
						
			x.append(float(line[0]))
			y.append(float(line[1]))
			z.append(float(line[2]))
			node_type.append(line[3])
			node_data = zip(x,y,z,node_type)
			# pdata[node_id] = node_data
			node_id +=1


	# mapped = CordToBinary(x,y,z)  

	# node_data,edge_data,special_edges = MapToGraph(mapped)

#	origin = node_data[0]
#	target = node_data[1]
	print(len(node_data))
	origin = [2,2,0,'o']
	target = [3.5,0.4,0,'t']

	cleaning_bot = gen_path(node_data,node_id,origin,target,threshold=0.03)

	cleaning_bot.build_graph()

	# cleaning_bot.Heurestics()

	optimal_path = cleaning_bot.master_path()
	print ("Path Planning Successful")
	time.sleep(1)
	if (display==1):
		cleaning_bot.display_path()

	if (animate==1):
		cleaning_bot.animate()

	print (cleaning_bot.return_path())
	
	f =  open("upload2.txt","w+")
	f.write("Path: " + str(cleaning_bot.return_path()) + '\n')
	url = os.getcwd() + '/temp-plot'
	f.write("URL: " + url)
	f.flush()
	f.close()

def parser_arguments():


	parser = argparse.ArgumentParser(description='Cleaning Bot Parser')
	parser.add_argument('--display',dest='display',type=int,default=0)
	parser.add_argument('--animate',dest='animate',type=int,default=1)
	parser.add_argument('--fil',dest='fil',type=str,default='wab.txt')
	return parser.parse_args()

if __name__ == '__main__':
	main(sys.argv)

   

