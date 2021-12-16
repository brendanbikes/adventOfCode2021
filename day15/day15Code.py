from collections import defaultdict
from heapq import *
import numpy as np
import sys

class Graph(object):
	def __init__(self):
		self.edges = defaultdict(list)
		self.weights = {}

	def add_edge(self, from_node, to_node, weight):
		self.edges[from_node].append(to_node)
		self.weights[(from_node, to_node)] = weight

def readInput():
	with open('./day15InputTest.txt', 'r') as f:
		data = [x.strip() for x in f.readlines()]

	i=0
	grid = {}

	for row in data:
		j=0
		for num in row:
			grid[(i,j)] = int(num)
			j+=1
		i+=1

	edges = makeEdges(grid)

	return grid, edges, len(data)

def makeEdges(grid):
	edges = []
	for key, val in grid.items():

		#west
		if grid.get((key[0],key[1]-1), 0):
			edges.append((key, (key[0], key[1]-1), grid.get((key[0],key[1]-1),0)))

		#east
		if grid.get((key[0],key[1]+1), 0):
			edges.append((key, (key[0], key[1]+1), grid.get((key[0],key[1]+1),0)))

		#north
		if grid.get((key[0]-1,key[1]), 0):
			edges.append((key, (key[0]-1, key[1]), grid.get((key[0]-1,key[1]),0)))

		#south
		if grid.get((key[0]+1,key[1]), 0):
			edges.append((key, (key[0]+1, key[1]), grid.get((key[0]+1,key[1]),0)))

	return edges

def readInputPart2():
	with open('./day15Input.txt', 'r') as f:
		data = [x.strip() for x in f.readlines()]

	i=0
	M = len(data) #size of tiles
	N = 5 #size of meta-grid
	grid = {}

	for row in data:
		j=0
		row = [int(x) for x in row]
		#replicate the row 4 additional times, increasing by 1, and wrapping >9 to 1

		temp = row[:] #this piece gets updated
		newRow = row[:] #this gets extended
		for k in range(N-1):
			temp = [x+1 if (x+1)<=9 else 1 for x in temp]
			newRow += temp

		#file this row
		for num in newRow:
			grid[(i,j)] = int(num)
			j+=1

		temp=newRow[:]
		#now replicate downward N times at M-size intervals
		for k in range(N-1):
			temp = [x+1 if (x+1)<=9 else 1 for x in temp]
			#file this row
			j=0
			for num in temp:
				grid[((k+1)*M+i,j)] = int(num)
				j+=1
		i+=1

	edges = makeEdges(grid)

	return grid, edges, len(data)*N

def dijkstraHeap(edges, f, t):
	g = defaultdict(list)
	for o, d, c in edges:
		g[o].append((c,d))

	q, visited, mins = [(0,f,[])], set(), {f: 0}

	while q:
		(cost,v1,path) = heappop(q)
		if v1 not in visited:
			visited.add(v1)
			path = [v1] + path
			if v1 == t:
				return (cost, path) #reached end yay

			for c, v2 in g.get(v1, ()):
				if v2 in visited:
					continue
				prev = mins.get(v2, None)
				next = cost + c
				if prev is None or next < prev:
					mins[v2] = next #update mincost with new lower cost node
					heappush(q, (next, v2, path))

	return (float("inf"), [])

def part1():
	#forward search for path from (0,0) to (M,M) with lowest possible score
	graph = Graph()
	grid, edges, M = readInput()
	for edge in edges:
		graph.add_edge(*edge)

	path = dijkstra(graph, (0,0), (M-1,M-1))

	risk = 0
	for x in path[1:]:
		risk += grid.get(x,0)

	print('The optimal path risk is {}'.format(risk))

def part2():
	#tile the input 4 additional times in both directions, increasing risks by 1 each time and wrapping from over 9 to 1
	grid, edges, M = readInputPart2()

	print(dijkstraHeap(edges,(0,0),(M-1,M-1)))

if __name__ == "__main__":
	part1()
	part2()