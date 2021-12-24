import sys
from itertools import chain

def readInput():
	with open('./day19Input.txt', 'r') as f:
		data = f.readlines()

	groups = []

	i=0
	for row in data:
		if '---' in row:
			#beginning divider
			#start new group
			new = []
		elif row == '\n':
			#end divider - file the existing group
			groups.append(new)

		elif i+1==len(data):
			new.append(tuple([int(x) for x in row.split(',')]))
			groups.append(new)
		else:
			#parse
			new.append(tuple([int(x) for x in row.split(',')]))
		i+=1

	return groups

def rotateCWZ(beacons):
	#rotates a set of beacon coordinates clockwise around the Z axis once
	#z coordinates do not change
	#new y coordinates are -x
	#new x coordinates are y
	return [(b[1],-b[0],b[2]) for b in beacons]

def rotateCWX(beacons):
	#rotates a set of beacon coordinates clockwise around the X axis once
	#x coordinates do not change
	#new z coordinates are -y
	#new y coordinates are z
	return [(b[0],b[2],-b[1]) for b in beacons]

def rotateCWY(beacons):
	#rotates a set of beacon coordinates clockwise around the Y axis once
	#y coordinates do not change
	#new z coordinates are -x
	#new x coordinates are z
	return [(b[2],b[1],-b[0]) for b in beacons]

def shift(beacons, origin=(0,0,0)):
	#shifts a set of beacon coordinates from assumed origin (0,0,0) to new origin (x,y,z)
	return [(b[0]+origin[0],b[1]+origin[1],b[2]+origin[2]) for b in beacons]

def rotate(beacons, rotation=(0,0,0)):
	#rotates a list of beacon coordinates
	#origin is the assumed origin location in (x,y,z) coordinate form
	#rotateX, rotateY, rotateZ inputs are numbers of rotations with the named axis as the axis of rotation
	#rotateZ ranges from 0 to 3
	#rotateX ranges from 0 to 3
	#rotateY is either 0, 1, or 3
	#This yields the number of rotational transformations of 24: 4 * 4 (X times Z) + 2 * 4 (Y times Z)

	#do the rotation
	for i in range(rotation[0]):
		beacons = rotateCWX(beacons)

	for i in range(rotation[1]):
		beacons = rotateCWY(beacons)

	for i in range(rotation[2]):
		beacons = rotateCWZ(beacons)

	return beacons


def match(beacons1, beacons2):
	#check if two sets of readings share at least 12 common coordinates
	if len(list(set(beacons1) & set(beacons2))) >= 12:
		return True
	else:
		return False

def part1():
	data = readInput()

	#setup rotation combinations
	X = [0,1,2,3]
	Y = [0,1,3]
	Z = [0,1,2,3]

	rotations = set()

	for x in X:
		for z in Z:
			rotations.add((x,0,z))

	for y in Y:
		for z in Z:
			rotations.add((0,y,z))

	#for each next unmapped set of beacon readings, iterate through all possible transformations to try and match it to one of the currently-mapped areas
	#the next set of beacon readings may NOT match a currently mapped area -- that is OK. Proceed to the next one if no match.
	#iterate through in a while loop, running until all unmapped regions become mapped

	#treat the first scanner reading as the initial mapped region, and the remaining as unmapped -- this algorithm will not care where it starts the search
	#when a new reading set is mapped, it's removed from the unmapped list, and its transformed coordinates are append to the mapped list
	#at the end, the mapped lists can be unified and made into a set, to yield the final list of all actual beacon sites
	mapped = [data[0]]
	unmapped = data[1:]
	scanners = [(0,0,0)]

	while unmapped:
		for u in unmapped:
			exit = False
			#try to map this to any of the existing mapped areas
			for m in mapped:
				#try and map u to m by transforming u
				#dynamically determine the range of possible shifts - try matching each combination of beacon readings in the pair - calculate the shift associated, and apply it
				#possible origins are up to r in all directions

				for rotation in rotations:
					temp = rotate(u, rotation=rotation)
					#wait=input()
					for b1 in m:
						for b2 in temp:
							#try to match this pair of beacons and see what happens
							dx = b1[0] - b2[0]
							dy = b1[1] - b2[1]
							dz = b1[2] - b2[2]

							temp2=shift(temp, origin=(dx,dy,dz))

							if match(m,temp2):
								#success! file the transformed coordinates in the mapped list, and remove the pre-transformed coordinates from the unmapped list
								mapped.append(temp2)
								scanners.append((dx,dy,dz))
								unmapped = [q for q in unmapped if q!=u]
								#set a break flag
								exit = True
								break
						if exit:
							break
					if exit:
						break
				if exit:
					break

		#if after 1 iteration we haven't mapped anything - break, there's an error
		if len(mapped) == 1:
			print('Error somewhere - program found no match')
			break

	#should have a totally mapped dataset now
	#find the number of beacons
	n = len(set(chain(*mapped)))
	print('The final number of beacons is ...{}'.format(n))

	return scanners

def part2():
	#calculate the largest manhattan distance between any two scanners
	scanners = part1()

	M = []
	for s1 in scanners:
		for s2 in scanners:
			m = s2[2]-s1[2] + s2[1]-s1[1] + s2[0]-s1[0]
			M.append(m)

	print('The maximum Manhattan distance between any two scanners is {}'.format(max(M)))

if __name__ == "__main__":
	#part1()
	part2()