import numpy as np

def readInput():
	with open('./day13Input.txt', 'r') as f:
		data = [x.strip() for x in f.readlines()]

	divider = data.index('')
	points = data[0:divider]
	folds = data[divider+1:]

	#process dots
	dots = set()
	for point in points:
		dots.add(tuple([int(x) for x in point.split(',')]))

	#process folds
	newFolds = []
	for fold in folds:
		tmp = fold.split(' ')[2]
		var = tmp[0]
		val = int(tmp[2:])
		newFolds.append((var, val))


	return dots, newFolds

def foldVertical(dots, val):
	for dot in list(dots):
		if dot[0] > val:
			d = dot[0] - val
			dots.add((val-d, dot[1]))
			dots.remove(dot)

	return dots

def foldHorizontal(dots, val):
	for dot in list(dots):
		if dot[1] > val:
			d = dot[1] - val
			dots.add((dot[0], val-d))
			dots.remove(dot)

	return dots

def part1():
	n = 1 #number of folds to do

	dots, folds = readInput()

	for axis, val in folds[:n]:
		print(axis,val)
		if axis == 'x':
			#fold along a vertical line
			#if point has x > fold[0] with distance d = x - fold[0], then it merges with value at fold[0] - x
			dots = foldVertical(dots, val)

		elif axis == 'y':
			#fold along a horizontal line
			dots = foldHorizontal(dots, val)


	print('There are {} remaining dots after {} folds.'.format(len(dots), n))

def part2():
	#do all folds

	dots, folds = readInput()

	for axis, val in folds:
		print(axis,val)
		if axis == 'x':
			#fold along a vertical line
			#if point has x > fold[0] with distance d = x - fold[0], then it merges with value at fold[0] - x
			dots = foldVertical(dots, val)

		elif axis == 'y':
			#fold along a horizontal line
			dots = foldHorizontal(dots, val)

	#print out the code output
	M = max([x[0] for x in dots] + [x[1] for x in dots]) + 1

	grid = [['.']*M for i in range(M)]

	for dot in dots:
		print(dot)
		grid[dot[1]][dot[0]] = '#'

	for line in grid:
		print(line)

if __name__ == "__main__":
	part1()
	part2()