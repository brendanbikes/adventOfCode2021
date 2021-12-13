from collections import Counter

def readInput():
	with open('./day12Input.txt', 'r') as f:
		data = f.readlines()

	map = []
	for node1, node2 in [x.strip().split('-') for x in data]:
		if node1 == 'start' or node2 == 'end':
			map.append((node1,node2))
		elif node1 == 'end' or node2 == 'start':
			map.append((node2,node1))
		else:
			map.append((node1,node2))
			map.append((node2,node1))

	return map

def recur(map, root, currentPath=[], paths=[]):
	if root == 'start':
		currentPath = []

	#append current node
	currentPath.append(root)

	if root == 'end':
		paths.append(currentPath)

	elif root.isupper() or (root.islower() and root not in currentPath[:-1]):
		nextNodes = [x[1] for x in map if (x[0]==root)]
		for next in nextNodes:
			#make new path copy due to branching
			nextPath = currentPath[:]
			recur(map, next, nextPath, paths)

	#all done!
	return paths

def recur2(map, root, currentPath=[], paths=[]):
	if root == 'start':
		currentPath = []

	#append current node
	currentPath.append(root)

	if root == 'end':
		paths.append(currentPath)

	elif root.isupper() or (root.islower() and len([x for x in dict(Counter([y for y in currentPath[:-1] if y.islower()])).values() if x > 1])==0) or (root.islower() and root not in currentPath[:-1]):
		nextNodes = [x[1] for x in map if (x[0]==root)]
		for next in nextNodes:
			#make new path copy due to branching
			nextPath = currentPath[:]
			recur2(map, next, nextPath, paths)

	#all done!
	return paths

def part1():
	#enumerate all paths that pass through small caves at most 1 time
	#probably going to need recursion

	map = readInput()

	paths = recur(map, 'start')

	print('\nThere are {} unique paths from start to finish.'.format(len(paths)))

def part2():
	#allowed 1 revisit to a small cave -- keep a global variable representing revisits to small caves

	map = readInput()

	paths = recur2(map, 'start')

	print('\nThere are {} unique paths from start to finish.'.format(len(paths)))

if __name__ == "__main__":
	part1()
	part2()