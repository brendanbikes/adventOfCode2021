def readInput():
	with open('./day9Input.txt', 'r') as f:
		data = f.readlines()

	return [x.strip() for x in data]

def part1():
	data = readInput()

	#put data into a dictionary
	grid = {}

	i=0
	for row in data:
		j=0
		for num in row:
			grid[(i,j)] = int(num)
			j+=1
		i+=1
	
	I = i
	J = j

	#find low points
	R = 0 #total risk
	for i in range(0,I):
		for j in range(0,J):
			q = grid.get((i,j))

			n = grid.get((i-1,j), 99)
			w = grid.get((i,j-1), 99)
			s = grid.get((i+1,j), 99)
			e = grid.get((i,j+1), 99)

			if q < w and q < n and q < e and q < s:
				#low point
				#risk
				r = q+1
				R+=r

	print('The total risk is {}.'.format(R))

def recur(grid, root, basin=set()): #root is (i,j,p)
	#recursive search of grid starting at root, identifying basins

	#print(root)

	#add root to basin
	basin.add(root)

	i=root[0]
	j=root[1]

	n=grid.get((i-1,j),0)
	w=grid.get((i,j-1),0)
	s=grid.get((i+1,j),0)
	e=grid.get((i,j+1),0)

	searchDirections=[]
	if n > root[2] and n < 9:
		searchDirections.append(tuple([i-1,j,n]))
	if w > root[2] and w < 9:
		searchDirections.append(tuple([i,j-1,w]))
	if s > root[2] and s < 9:
		searchDirections.append(tuple([i+1,j,s]))
	if e > root[2] and e < 9:
		searchDirections.append(tuple([i,j+1,e]))

	for x in searchDirections:
		basin.add(x)
		recur(grid, x, basin=basin)

	return len(basin)

def part2():
	data = readInput()

	#put data into a dictionary
	grid = {}

	i=0
	for row in data:
		j=0
		for num in row:
			grid[(i,j)] = int(num)
			j+=1
		i+=1

	
	I = i
	J = j

	#find low points

	Q = []

	R = 0 #total risk
	for i in range(0,I):
		for j in range(0,J):
			q = grid.get((i,j))

			n = grid.get((i-1,j), 99)
			w = grid.get((i,j-1), 99)
			s = grid.get((i+1,j), 99)
			e = grid.get((i,j+1), 99)

			if q < w and q < n and q < e and q < s:
				#low point
				Q.append(tuple([i,j,q]))

	sizes=[]
	print(Q)
	for p in Q:
		size = recur(grid, p, basin=set())
		sizes.append(size)

	#find 3 largest basins and multiply them
	sizes.sort(reverse=True)
	print('The multiplied basin sizes is {}'.format(sizes[0]*sizes[1]*sizes[2]))

if __name__ == "__main__":
	part1()
	part2()