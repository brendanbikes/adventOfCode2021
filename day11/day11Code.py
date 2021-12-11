from math import ceil, floor
from time import sleep

#globals
M=10
N=100

def readInput():
	with open('./day11Input.txt', 'r') as f:
		data = f.readlines()

	return [x.strip() for x in data]


def findFlashers(grid, flashed=[]):
	flashers = []
	for i in range(M):
		for j in range(M):
			if grid.get((i,j), 0) > 9 and tuple([i,j]) not in flashed:
				flashers.append((i,j))

	return flashers

def printGrid(grid):
	print('\n')
	for i in range(M):
		print([grid.get((i,j)) for j in range(M)])

def part1():
	data = readInput()

	#put data into a 10x10 grid
	grid = {}

	print(M)

	for i in range(M):
		for j in range(M):
			grid[(i,j)] = int(data[i][j])

	#count number of flashes after 100 steps
	flashCount=0

	for n in range(N):
		printGrid(grid)
		#first, increase energy level of the entire grid
		for i in range(M):
			for j in range(M):
				grid[(i,j)] += 1

		#now do flashing in a while loop

		printGrid(grid)

		#find initial flashers
		flashers = findFlashers(grid)
		flashCount += len(flashers)
		
		flashed = []

		while len(flashers) > 0:
			neighbors = []
			for flasher in flashers:
				#set this value to 0 and log it as flashed
				grid[flasher] = 0
				flashed.append(flasher)

			for flasher in flashers:
				#find neighbors - they can appear more than once
				for i in range(max(0, flasher[0]-1), min(M, flasher[0]+2)):
					for j in range(max(0, flasher[1]-1), min(M, flasher[1]+2)):
						print((i,j))
						#print('\n neighbor')
						#print((i,j))
						if tuple([i,j]) not in flashed:
							#octopi that have already flashed this step are not eligible to do so again
							neighbors.append(tuple([i,j]))

			#increase energy of all neighbors simultaneously

			#print(neighbors)
			for neighbor in neighbors:
				print(neighbor)
				grid[neighbor] += 1

			#now, find new set of flashers and loop
			flashers = findFlashers(grid, flashed=flashed)

			#increase the count
			flashCount += len(flashers)

			printGrid(grid)

	print('At the end of {} steps, the total number of flashes was {}'.format(N, flashCount))

def part2():
	#find first simultaneous flash

	data = readInput()

	#put data into a 10x10 grid
	grid = {}

	print(M)

	for i in range(M):
		for j in range(M):
			grid[(i,j)] = int(data[i][j])

	flashers = []

	z=0

	while True:
		z+=1
		printGrid(grid)
		flashCount=0
		#first, increase energy level of the entire grid
		for i in range(M):
			for j in range(M):
				grid[(i,j)] += 1

		#now do flashing in a while loop

		#find initial flashers
		flashers = findFlashers(grid)
		flashCount+=len(flashers)
		
		flashed = []
		while len(flashers) > 0:
			neighbors = []
			for flasher in flashers:
				#print('\nflasher')
				#print(flasher)
				#set this value to 0 and log it as flashed
				grid[flasher] = 0
				flashed.append(flasher)

			for flasher in flashers:
				#find neighbors - they can appear more than once
				for i in range(max(0, flasher[0]-1), min(M, flasher[0]+2)):
					for j in range(max(0, flasher[1]-1), min(M, flasher[1]+2)):
						if tuple([i,j]) not in flashed:
							#octopi that have already flashed this step are not eligible to do so again
							neighbors.append(tuple([i,j]))

			#increase energy of all neighbors simultaneously
			for neighbor in neighbors:
				#print(neighbor)
				grid[neighbor] += 1

			#now, find new set of flashers and loop
			#this step will never yield a simultaneous flash, because the flashed array is nonempty
			flashers = findFlashers(grid, flashed=flashed)
			flashCount+=len(flashers)

		if flashCount==100:
			print('All octopi flash together on step {}'.format(z))
			break

if __name__ == "__main__":
	part1()
	part2()