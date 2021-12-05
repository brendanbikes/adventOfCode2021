def readInput():
	with open('./day5Input.txt', 'r') as f:
		data = f.readlines()

	lines = []
	for row in data:
		pairs = [x.split(',') for x in row.strip().split(' -> ')]
		lines.append([(int(pairs[0][0]), int(pairs[0][1])), (int(pairs[1][0]), int(pairs[1][1]))])

	return lines

def part1():
	lines = readInput()

	#set up grid as a dictionary
	grid = {}

	for line in lines:
		(x1, y1), (x2, y2) = line
		#test if line is horizontal or vertical
		if x1==x2 or y1==y2:
			#get all points that will get +1
			xcoords = [z for z in range(min(x1,x2), max(x1,x2)+1)] #include endpoint
			ycoords = [z for z in range(min(y1,y2), max(y1,y2)+1)] #include endpoint

			for x in xcoords:
				for y in ycoords:
					if grid.get((x,y), None) is not None:
						grid[(x,y)] += 1
					else:
						#initialize new grid point
						grid[(x,y)] = 1

	#count the number of grid points with a value of 2
	print('The number of grid points with 2 intersecting thermal vent lines is {}.'.format(len([z for z in grid.values() if z >= 2])))

def part2():
	#consider diagonal lines
	lines = readInput()

	#set up grid
	grid = {}

	for line in lines:
		(x1, y1), (x2, y2) = line
		#test if line is horizontal, vertical
		if x1==x2 or y1==y2:
			xcoords = range(min(x1,x2), max(x1,x2)+1) #include endpoint
			ycoords = range(min(y1,y2), max(y1,y2)+1) #include endpoint

			for x in xcoords:
				for y in ycoords:
					if grid.get((x,y), None) is not None:
						grid[(x,y)] += 1
					else:
						#initialize new grid point
						grid[(x,y)] = 1

		#now test if line is diagonal
		elif abs(x2-x1) == abs(y2-y1):
			xcoords = [z for z in range(min(x1,x2), max(x1,x2)+1)]
			ycoords = [z for z in range(min(y1,y2), max(y1,y2)+1)]

			if x2 < x1:
				xcoords.reverse()

			if y2 < y1:
				ycoords.reverse()

			#zip together
			coords = zip(xcoords, ycoords)

			for x,y in coords:
				if grid.get((x,y), None) is not None:
					grid[(x,y)] += 1
				else:
					#initialize new grid point
					grid[(x,y)] = 1

	#count the number of grid points with a value of 2
	print('The number of grid points with 2 intersecting thermal vent lines is {} when including diagonals.'.format(len([z for z in grid.values() if z >= 2])))

if __name__ == "__main__":
	part1()
	part2()