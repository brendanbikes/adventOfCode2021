

def readInput():
	with open('./day3Input.txt', 'r') as f:
		data = f.readlines()

	return [x.strip() for x in data]

def part1():
	data = readInput()

	n = len(data[0]) #length of numbers
	m = len(data) #number of numbers - if sum of array of ith digits is greater than half this, then 1 is the most common bit

	i = 0

	gamma = ''
	epsilon = ''

	while i < n:
		#get the ith numbers in an array and find the most/least common bits
		nums = [int(x[i]) for x in data]
		if sum(nums) > m/2:
			#1 is most common bit
			gamma += str(1)
			epsilon += str(0)

		else:
			#0 is most common bit
			gamma += str(0)
			epsilon += str(1)
		i+=1


	#now convert the binary strings to decimal and multiply
	gamma = int(gamma, 2)
	epsilon = int(epsilon, 2)

	print('The gamma rate is {} and the epsilon rate is {}. Their product is {}.'.format(gamma, epsilon, gamma*epsilon))


def part2():
	data = readInput()

	n = len(data[0])
	m = len(data)

	#first, find the oxygen generator rating - iterative search using most common bits

	retained = data #seed

	i=0 #bit position for search

	while len(retained) > 1:
		m = len(retained)
		nums = [int(x[i]) for x in retained]
		if sum(nums) >= m/2:
			#1 is most common bit or there is a tie - retain all numbers with 1 in position i
			retained = [x for x in retained if x[i] == '1']

		else:
			#0 is most common bit - retain all numbers with 0 in position i
			retained = [x for x in retained if x[i] == '0']

		i+=1

	ox = int(retained[0],2)

	#second, find the C02 scrubber rating - iterative search using least common bits

	i=0 #bit position for search

	retained = data #seed

	while len(retained) > 1:
		m = len(retained)
		nums = [int(x[i]) for x in retained]
		if sum(nums) >= m/2:
			#1 is the most common bit or there is a tie - retain all numbers with 0, the opposite, in position i
			retained = [x for x in retained if x[i] == '0']

		else:
			#0 is the most common bit - retain all numbers with 1, the opposite, in position i
			retained = [x for x in retained if x[i] == '1']

		i+=1

	c02 = int(retained[0],2)

	print('The oxygen generator rating is {}. The C02 scrubber rating is {}. Their product is {}.'.format(ox, c02, ox*c02))


if __name__ == "__main__":
	part1()
	part2()