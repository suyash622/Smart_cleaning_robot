import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
import sys

class gen_path(object):
	def __init__(node_data,edge_data,special_edges):
		self.node_data=node_data
		self.edge_data=edge_data
		self.special_nodes=special_edges
		self.path=[]
		self.origin = origin
		self.target =target	
		self.priority = []
		self.G=nx.Graph()


	def build_graph(self):
		for i in node_data:
			self.G.add_node(i)
		for e in edge_data:
			n1 = e[0]
			n2 = e[1]
			weight = e[3]
			self.G.add_edge(n1,n2)
			self.G[n1][n2]['weight'] = self.weight_calculate(n1,n2)

	def Heurestics(self):
		for i in special_edges:
			self.priority.append(i)

	def weight_calculate(self,n1,n2):
		return (n1[0]-n2[0])**2 + (n1[1]-n2[1])**2

	def master_path(self):
		pass

	def display_path(self):
		x =[]
		y =[]
		for i in self.path;
			x.append(i[0])
			y.append(i[1])
		plt.plot(x,y,'-ro')
		plt.gca().set_aspect('equal', adjustable='box')
		plt.show()

	def master_path(self):
		self.path =nx.dijkstra_path(self.G,source=self.origin,target=self.target)
		for pos,part_path in enumerate(self.path):
			x_off,y_off,done = self.isobstacle(part_path):
			if done:
				self.modify_path(pos,x_off,y_off)

	def modify_path(self,pos,x,y):
		self.path.insert(pos,[x,y])

	def isobstacle(self,part_path):
		p1 = part_path[1]
		p2 = part_path[0]

		for p3 in self.node_data:
			d = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)
			if (d < threshold):
				x4 = x3 - (threshold-d)* (p1[1]-p2[1])
				y4 = y3 + (threshold-d) * (p1[0]-p2[0])
				return x4,y4,True
		
		return 0,0,False

	def animate(self):
		x =[]
		y =[]
		for i in self.path:
			x.append(i[0][0],i[1][0])
			y.append(i[1][0],i[1][1])




		data=[dict(x=x, y=y, 
           mode='lines', 
           line=dict(width=2, color='blue')
          ),
     	 dict(x=x, y=y, 
           mode='lines', 
           line=dict(width=2, color='blue')
          )
    	]

    	xm = np.min(np.array(x)) - 0.05
    	xM = np.max(np.array(x)) + 0.05
    	ym = np.min(np.array(x)) - 0.05
    	yM = np.max(np.array(y)) + 0.05 


    	layout=dict(xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
            yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
            title='Path of the Cleaning robot', hovermode='closest',
            updatemenus= [{'type': 'buttons',
                           'buttons': [{'label': 'Play',
                                        'method': 'animate',
                                        'args': [None]}]}])


    	frames=[dict(data=[dict(x=[xx[k]], 
                        y=[yy[k]], 
                        mode='markers', 
                        marker=dict(color='red', size=10)
                        )
                  ]) for k in range(N)]    


    	figure1=dict(data=data, layout=layout, frames=frames)          
		plotly.offline.plot(figure1)



		

def readFile(path):
    return open(path, 'rt')

def CordToBinary(x,y,z):
	pass

def MapToGraph(mapped):  # Use OpenCV's connected components
	pass

def main(args):


	args = parser_arguments()
	display = args.display
	animate = args.animate

	inputFile = readFile('./points.pcd')
	inputString = inputFile.read()

	x = []
	y = []
	z = []
	for line in inputString.splitlines():
		line = line.split(' ')
		if line[0]!='#' and line[0].isalpha()==False:
		 
			x.append(float(line[0]))
			y.append(float(line[1]))
			z.append(float(line[2]))	

	mapped = CordToBinary(x,y,z)	

	node_data,edge_data,special_edges = MapToGraph(mapped)

	cleaning_bot = gen_path(node_data,edge_data,special_edges)

	cleaning_bot.build_graph()

	cleaning_bot.Heurestics()

	optimal_path = cleaning_bot.master_path()

	if (display):
		cleaning_bot.display_path()

	if (animate):
		cleaning_bot.animate()

def parser_arguments():


    parser = argparse.ArgumentParser(description='Cleaning Bot Parser')
    parser.add_argument('--display',dest='display',type=bool,default=True)
    parser.add_argument('--animate',dest='animate',type=bool,default=True)
    return parser.parse_args()

if __name__ == '__main__':
    main(sys.argv)


