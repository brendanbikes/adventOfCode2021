def readInput():
	with open('./day7Input.txt', 'r') as f:
		data = f.readlines()

	row = data[0].split(',')

	return [int(x) for x in row]


def part1():
	data = readInput()
	#determine minimum sum of differences between all numbers and a number in min(array), max(array)

	print(data)
	fuelCosts = {}
	for i in range(min(data), max(data)):
		#print(i)
		#suppose this is the consolidation point
		for k in data:
			#calculate fuel cost for this crab
			d = abs(k - i)
			fuelCosts[i] = fuelCosts.get(i, 0) + d

	print(fuelCosts)

	#find the minimum
	print('This is the minimum fuel cost: {}'.format(min([x for x in fuelCosts.values()])))


def part2():
	data = readInput()

	fuelCosts = {}
	#probably a better way to do this...return to optimize later
	for i in range(min(data), max(data)):
		#suppose this is the consolidation point
		for k in data:
			#calculate fuel cost for this crab
			d = abs(k-i)
			d = sum([x for x in range(1,abs(k-i)+1)])
			fuelCosts[i] = fuelCosts.get(i, 0) + d

		#[sum([x for x in range(1,abs(k-i)+1)]) for k in data]

	#find the minimum
	print('This is the minimum fuel cost: {}'.format(min([x for x in fuelCosts.values()])))




if __name__ == "__main__":
	part1()
	part2()