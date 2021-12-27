import sys
import os

def readInput():
	with open('./day25Input.txt', 'r') as f:
		data = [x.strip() for x in f.readlines()]

	grid = {}

	i=0
	for row in data:
		j=0
		for x in row:
			grid[(i,j)] = x
			j+=1
		i+=1

	return grid, i, j

def getNext(grid,coords):
	#fetches the coordinates of the next spot and returns them, but only if it corresponds to a valid move
	if grid.get(coords,'.') == '>':
		if grid.get((coords[0],coords[1]+1), '') == '.':
			#next spot exists and is open
			return (coords[0],coords[1]+1)

		elif grid.get((coords[0],coords[1]+1), ''):
			#next spot exists but is occupied
			return coords

		elif grid.get((coords[0],0)) == '.':
			#next spot didn't exist - wrap around spot is open
			return (coords[0],0)

		else:
			#wrap-around spot wasn't open
			return coords

	elif grid.get(coords,'.') == 'v':
		if grid.get((coords[0]+1, coords[1]), '') == '.':
			#next spot exists and is open
			return (coords[0]+1, coords[1])
	
		elif grid.get((coords[0]+1,coords[1]), ''):
			#next spot exists but is occupied
			return coords

		elif grid.get((0,coords[1])) == '.':
			#next spot didn't exist = wrap around spot is open
			return (0, coords[1])

		else:
			#wrap-around spot wasn't open
			return coords

	else:
		#this patch of seafloor was empty
		return False

def render(grid):
	os.system('cls' if os.name=='nt' else 'clear')
	for i in sorted(list(set([x[0] for x in grid.keys()]))):
		row = []
		for j in sorted(list(set([x[1] for x in grid.keys()]))):
			row.append(grid.get((i,j)))
		print(''.join(row))

def fillSeafloor(grid, M, N):
	for i in range(M):
		for j in range(N):
			if not grid.get((i,j), ''):
				grid[(i,j)] = '.'

	return grid

def part1():
	grid, M, N = readInput()

	render(grid)

	n=0
	while True:
		#first step is to get all Next spaces for all the sea cucumbers in the current grid
		#make new copy of grid

		newGrid = {}
		for key, val in grid.items():
			if val == '>':
				if getNext(grid, key):
					#either a valid next move for (i,j) or the sea cucumber stays put
					newGrid[getNext(grid, key)] = val
			elif val == 'v':
				#hold the south-facing sea cucumbers for now
				newGrid[key] = val

		#backfill seafloor
		newGrid = fillSeafloor(newGrid, M, N)

		#now move the south-facing herd -- careful to read from the new grid
		newGrid2 = {}
		for key, val in newGrid.items():
			if val == 'v':
				if getNext(newGrid, key):
					#either a valid next move for (i,j) or the sea cucumber stays put
					newGrid2[getNext(newGrid, key)] = val
			elif val == '>':
				#hold the east-facing sea cucumbers
				newGrid2[key] = val

		#backfill seafloor
		newGrid2 = fillSeafloor(newGrid2, M, N)

		#update number of steps taken
		n+=1

		#test if any moves were made -- the sets of dictionary items should be different
		if set(grid.items()) == set(newGrid2.items()):
			#no moves were made
			break

		#if moves were made, continue the process
		#file the new grid back
		grid = newGrid2.copy()

		render(grid)

	print('The sea cucumbers stopped moving after {} steps.'.format(n))


	#find the first step on which the sea cucumbers stop moving

def part2():
	pass


if __name__ == "__main__":
	part1()
	part2()