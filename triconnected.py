from sage.graphs.graph import Graph
from collections import deque
from enum import Enum

class ArrayInfo:
	def __init__(self, vertices, list_of_degrees):
		"""
			- vertices:    it stores the list of vertices of the input graph.
			- m_numCount:  It stores the count of vertices visited in a DFS run
			- m_NUMBER:    it stores the order in which vertices was visited in a DFS run.
			- m_LOWPT1(v): it stores the vertex u, where u is the lowest vertex reachable from  v by traversing 0 or more tree arcs in DFS tree,
			- m_LOWPT2(v): it stores the vertex u, where u is the second lowest vertex reachable from  v by traversing 0 or more tree arcs followed by at most frond in DFS tree,
			- m_FATHER(v): it stores the vertex u, where u is the father in DFS tree of G.
			- m_ND(v):     it stores number of proper descendants of v.
			- m_DEGREE:    it stores degree of each vertex.
			- s1: first vertex of separation pair if G is biconnected, cut vertex of G if G is not biconnected, False if G is not connected.
			- s2: second vertex of separation pair if G is biconnected, False otherwise.
		"""
		self.vertices = vertices
		self.m_numCount = 0
		self.m_NUMBER   = {}
		self.m_LOWPT1   = {}
		self.m_LOWPT2   = {}
		self.m_FATHER   = {}
		self.m_ND       = {}
		self.m_DEGREE   = {}
		self.m_NODEAT   = {}
		self.s1 = False
		self.s2 = False

		for i in range(len(self.vertices)):
			self.m_NUMBER[self.vertices[i]] = 0
			self.m_LOWPT1[self.vertices[i]] = 0
			self.m_LOWPT2[self.vertices[i]] = 0
			self.m_FATHER[self.vertices[i]] = 0
			self.m_ND[self.vertices[i]]     = 0
			self.m_NODEAT[self.vertices[i]] = 0
			self.m_DEGREE[self.vertices[i]] = list_of_degrees[i]

class Search:
	"""
	graph : It's the input graph
	firstson_bool: it's boolean value to check weather firstson_value is initilized\
	visited_edges(u,v): It indicates weather u,v edge is visited or not. 
	"""
	
	def __init__(self, graph, array_info):
		self.graph = graph
		self.array_info = array_info
		self.firstson_bool = False
		self.firstSon_value = -1
		self.s1 = -1
		self.visited = {}
		self.visited_edges = {}
		self.init_visited_array()

	def init_visited_array(self):
		for i in self.array_info.vertices:
			self.visited[i] = False

		l = self.graph.edges()
		for i in l:
			self.visited_edges[i[0],i[1]] = False
			self.visited_edges[i[1],i[0]] = False
			
	def DFS1(self, v, u):

		"""
			v = the current vertex need to expand.
			u = parent of v, for firstnode v, u is initilize to false.
		"""
		self.array_info.m_numCount += 1
		self.array_info.m_NUMBER[v] = self.array_info.m_numCount
		self.array_info.m_FATHER[v] = u
		self.array_info.m_LOWPT1[v] = self.array_info.m_LOWPT2[v] = self.array_info.m_NUMBER[v]
		self.array_info.m_ND[v] = 1
		#self.visited[v] = True
		for neighbor in g.neighbors(v):
			if(not self.visited_edges[v, neighbor]):
				if(not self.array_info.m_NUMBER[neighbor]):
					self.visited_edges[v,neighbor] = True
					self.visited_edges[neighbor,v] = True
					if(not self.firstson_bool):
						self.firstSon_value = neighbor
						self.firstson_bool = True
					
					#self.array_info.m_TREE_ARC[neighbor] = e

					self.DFS1(neighbor, v)

					if(self.array_info.m_LOWPT1[neighbor] >= self.array_info.m_NUMBER[v] and (neighbor != self.firstSon_value or u != False)):
						self.array_info.s1 = v
				
					if (self.array_info.m_LOWPT1[neighbor] < self.array_info.m_LOWPT1[v]):
						self.array_info.m_LOWPT2[v] = min(self.array_info.m_LOWPT1[v],self.array_info.m_LOWPT2[neighbor])
						self.array_info.m_LOWPT1[v] = self.array_info.m_LOWPT1[neighbor]

					elif (self.array_info.m_LOWPT1[neighbor] == self.array_info.m_LOWPT1[v]):
						self.array_info.m_LOWPT2[v] = min(self.array_info.m_LOWPT2[v],self.array_info.m_LOWPT2[neighbor])

					else:
						self.array_info.m_LOWPT2[v] = min(self.array_info.m_LOWPT2[v],self.array_info.m_LOWPT1[neighbor])

					self.array_info.m_ND[v] += self.array_info.m_ND[neighbor]

				else:
					self.visited_edges[v,neighbor] = True
					self.visited_edges[neighbor,v] = True
					if (self.array_info.m_NUMBER[neighbor] < self.array_info.m_LOWPT1[v]):
						self.array_info.m_LOWPT2[v] = self.array_info.m_LOWPT1[v]
						self.array_info.m_LOWPT1[v] = self.array_info.m_NUMBER[neighbor]

					elif (self.array_info.m_NUMBER[neighbor] > self.array_info.m_LOWPT1[v]):
						self.array_info.m_LOWPT2[v] = min(self.array_info.m_LOWPT2[v],self.array_info.m_NUMBER[neighbor])

def istriconnected(graph):

	"""
	n and m are number of nodes and edges respectively
	"""
	n = graph.num_verts()
	m = graph.num_edges()

	if(n==0):
		return True

	#All the safe loops and multiple edges will be removed.
	graph.remove_loops()
	graph.remove_multiple_edges()

	vertices         = graph.get_vertices().keys()
	list_of_degrees  = graph.degree() 

	m_start = vertices[0]
	
	array_info = ArrayInfo(vertices, list_of_degrees)

	search = Search(graph, array_info)

	# False means m_start is root of the tree.
	search.DFS1(m_start, False) 

	for i in range(n):
		print i, array_info.m_NUMBER[i]

	print "-----------------------------"
	for i in range(n):
		print i, array_info.m_LOWPT1[i]

	print "-----------------------------"
	for i in range(n):
		print i, array_info.m_LOWPT2[i]

	#graph is not connected
	if(array_info.m_numCount < n):
		print "Graph is not connected"
		return False

	print "s1 = ", array_info.s1, " m_numCount = ", array_info.m_numCount

	#s1 is a cut vertex
	if(array_info.s1 != False):
		return False


if __name__ == '__main__':
	g = Graph([[0, 1], [1, 2], [2, 0], [0, 3], [1, 7], [1, 4], [1, 5], [3, 6], [2, 0], [2, 3], [1, 0], [3, 9], [4, 0], [1, 3], [4, 2], [5, 0], [6, 2], [4, 8], [0, 2], [7, 2], [4, 1], [8, 6], [9, 1], [2, 3], [5, 9], [9, 4], [5, 8], [8, 3], [8, 2], [4, 3], [0, 0]])
	tri = istriconnected(g)