from collections import deque

def readInput():
	with open('./day22Input.txt', 'r') as f:
		data = f.readlines()

	instructions = []

	for line in data:
		command, ranges = line.split(' ')
		xr, yr, zr = [r[2:].split('..') for r in ranges.split(',')]

		xmin = int(xr[0])
		xmax = int(xr[1])
		ymin = int(yr[0])
		ymax = int(yr[1])
		zmin = int(zr[0])
		zmax = int(zr[1])

		instructions.append([command, (xmin, ymin, zmin, xmax, ymax, zmax)])

	return instructions

def isEmpty(c):
	#unpack
	(cx1,cy1,cz1, cx2,cy2,cz2) = c
	#tests whether a cuboid has 0 volume
	#a cuboid will  if it has 0 distance in any of its 3 directions
	return True if (cx1==cx2 or cy1==cy2 or cz1==cz2) else False

def intersect(a,b):
	#tests whether two cuboids intersect at all
	#two squares will intersect with nonzero area if the leftmost right edge is to the right of the rightmost left edge, and
	#if the bottommost top edge is to the top of the topmost bottom edge
	#cannot just be touching -- has to overlap

	#unpack
	(ax1, ay1, az1, ax2, ay2, az2) = a
	(bx1, by1, bz1, bx2, by2, bz2) = b
	#extending this to 3D gives the following

	return True if (min(ax2,bx2) > max(ax1,bx1) and min(ay2,by2) > max(ay1,by1) and min(az2,bz2) > max(az1,bz1)) else False

def volume(cuboids):
	#computes the volume of all cuboids in a list
	v = 0
	for c in cuboids:
		#unpack
		(x1, y1, z1, x2, y2, z2) = c
		v+=(x2-x1)*(y2-y1)*(z2-z1)
	return v

def difference(a,b):
	#get the difference of two cuboid regions - it's already been determined that these do intersect with nonzero volume
	#cuboid A is the one that's assumed to be currently filed, and needs to be clipped to B and split up
	#function will return the set of new cuboids describing the region of A minus B
	#there can be up to 6 sub-cuboids - the top cut, the bottom cut, the two sides, and front and rear plugs
	#because we are dealing with a discrete lattice, these subcuboids must "shrink" away from the new cuboid by 1, to avoid double-counting

	#unpack
	(ax1,ay1,az1, ax2,ay2,az2) = a
	(bx1,by1,bz1, bx2,by2,bz2) = b

	#clip b to the bounds of a - take the rightmost left edge, leftmost right edge, bottommost top edge, etc.
	(bx1,by1,bz1, bx2,by2,bz2) = (
		max(ax1,bx1), max(ay1,by1), max(az1,bz1),
		min(ax2,bx2), min(ay2,by2), min(az2,bz2)
	)

	#now define new cuboids
	cuboids = [
		(ax1,ay1,az1, ax2,ay2,bz1), #bottom - bottom inner left corner of A to outer right corner of A, at height bottom of B
		(ax1,ay1,bz2, ax2,ay2,az2), #top - inner left corner of A, at height top of B, to top/outer right corner of A
		(bx1,ay1,bz1, ax2,by1,bz2), #front piece to the right
		(bx2,by1,bz1, ax2,ay2,bz2), #right piece to the back
		(ax1,by2,bz1, bx2,ay2,bz2), #back piece to the left
		(ax1,ay1,bz1, bx1,by2,bz2), #left piece to the front
	]

	return [x for x in cuboids if not isEmpty(x)]

def part1():
	instructions = readInput()

	#print(instructions)

	#initiate grid
	grid = {}

	for instruction in instructions:
		command, ranges = instruction
		xmin, ymin, zmin, xmax, ymax, zmax = ranges

		#filter -- only pay attention to the initialization region
		xr = [t for t in range(xmin,xmax+1) if t in range(-50,51)]
		yr = [t for t in range(ymin,ymax+1) if t in range(-50,51)]
		zr = [t for t in range(zmin,zmax+1) if t in range(-50,51)]

		for x in xr:
			for y in yr:
				for z in zr:
					grid[(x,y,z)] = 1 if command == 'on' else 0

	#count number of 'on' cubes
	print('The number of cubes turned on is {}'.format(len([c for c in grid.values() if c == 1])))


def part2():
	#need to pay attention to the entire reactor region -- can we define a new data structure that yields the current count of 'on' cubes, without keeping track of their individual states?
	#or maybe we can consolidate all the commands - roll them up into one summation by grouping all the 'on' commands 

	#every grouping of N consective 'on' commands can be lump-grouped together, and all x, y, z ranges consolidated by taking the maximums
	#then, once an 'off' command is received, find the intsercting subset of the off command



	#in general, when we add a new cuboid of "on" region, we check if this next cuboid intersects any of the existing cuboids
	#if there is no intersection, we simply add this cuboid to the list of "on" cuboid regions
	#if there is an intersection, we split the intersecting cuboid that's currently in the list of "on" cuboids, by clipping it to the bounds of the new cuboid
	#these smaller cuboids REPLACE the filed cuboid we were comparing
	#if we use a deque to store the cuboids, then when we compare a new cuboid B and there is no intersection with cuboid A, move A from right end of deque to left by doing pop and appendleft
	#If we split cuboid A into A1,A2...A6, then do pop() and extendleft([A1,A2,...,A6])
	#There are at most N possible comparison operations to do, where N is the number of cuboids at the start of comparing the next new cuboid B 
	#Once we complete this process for all cuboids currently in the list, do append(B) to add the cuboid we just compared

	#When we encounter an "off" cuboid C, need to test all filed cuboids for intersection
	#If C does not intersect any currently filed cuboids, great! Do nothing.
	#If C DOES intersect any currently filed "on" cuboids, do the same process as above for an "on" region but DO NOT APPEND C to the deque


	#cuboids are defined as lists of two tuples, representing their extent corner coordinates (x1,y1,z1) and (x2,y2,z2)
 
	instructions = readInput()

	#keep a scrolling list of "on" regions
	on = deque()

	for command, nextCuboid in instructions:
		#careful -- expand the x,y,z max by 1 to translate from point coordinates to coordinates of containing volume
		#e.g. a cube of (0,0,0) (0,0,0) is now (0,0,0), (1,1,1) giving it a volume of (1-0)^3 = 1
		#so now if a cube is actually (x1,y1,z1) = (x2,y2,z2) it has volume zero

		nextCuboid = (nextCuboid[0], nextCuboid[1], nextCuboid[2], nextCuboid[3]+1, nextCuboid[4]+1, nextCuboid[5]+1)
		#check if this instruction's cuboid region intersects any of the existing cuboids in on
		if len(on) == 0:
			#append first element
			on.append(nextCuboid)
			continue

		n = len(on) #number of operations to do

		for i in range(n):
			if intersect(on[-1], nextCuboid):
				#non-empty intersection - split
				subCuboids = difference(on[-1], nextCuboid)
				#pop the previously filed Cuboid from the deque
				on.pop()
				#append new subCuboids to the left of the deque
				on.extendleft(subCuboids)

			else:
				#no intersection - rotate the deque once
				on.rotate(1)
				
		#handle nextCuboid -- add it to the deque only if command was 'on'
		if command == 'on':
			on.appendleft(nextCuboid)

		#print(volume(on))


	#at the end, calculate total volume of 'on' regions

	print('The total volume of active reactor space is {}'.format(volume(on)))

if __name__ == "__main__":
	#part1()
	part2()