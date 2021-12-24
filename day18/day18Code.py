
import sys
import ast
from math import floor, ceil
from itertools import permutations


def readInput():
	with open('./day18Input.txt', 'r') as f:
		data = [ast.literal_eval(x) for x in f.readlines()]

	return data

def flatten(num, depth=0):
	#flatten a snailfish number into a list of tuples, where the first value is the number itself, and the second value is its depth in the structure
	#if depth is 0, number is in the root list
	l = []

	depth+=1
	for x in num:
		if isinstance(x,list):
			#go deeper
			l += flatten(x, depth)

		else:
			l.append((x,depth))

	return l

def increaseDepth(num):
	i=0
	for x in num:
		num[i] = (num[i][0], num[i][1] + 1)
		i += 1

	return num

def reduce(num):
	#reduce a given snailfish number
	#numbers with a depth of 5 indicate that that number's pair, at a depth of 4, is nested inside 4 other lists
	
	#step 1: scan through the list to identify the first/left-most pair of numbers with number-depth 5
	#explode any 1 pair 
	
	while True:
		if 5 in [x[1] for x in num]:
			#have at least 1 pair of numbers at number-depth 5 - explode the leftmost one found
			pair = []
			i=0
			for x in num:
				if x[1]==5 and len(pair)<2:
					pair.append(x[0])
				elif len(pair) == 2:
					break
				i+=1

			i = i-2
			#i is the list index of the deep pair of numbers, i is first number, i+1 is second number
			#explode this pair

			if i>0:
				depth = num[i-1][1]
				num[i-1] = (num[i-1][0]+pair[0], num[i-1][1])
			try:
				depth = num[i+2][1]
				num[i+2] = (num[i+2][0]+pair[1], num[i+2][1])
			except IndexError:
				pass

			#replace the existing pair at i and i+1 with a 0 at 1 less depth
			num[i] = (0,num[i][1]-1)
			try:
				num = num[:i+1] + num[i+2:]
			except IndexError:
				num = num[:i+1]

		elif not all(x[0] < 10 for x in num):
			#scan for numbers greater than 10 and split the leftmost one

			i=0
			for x in num:
				if x[0]>=10:
					z = x[:]
					break
				i+=1

			#split number at index i - replace it with a pair of numbers, the left is /2 rounded down, right is /2 rounded up
			left = [(int(floor(z[0]/2)), z[1]+1)]
			right = [(int(ceil(z[0]/2)), z[1]+1)]

			#reconstruct the list
			try:
				num = num[:i] + left + right + num[i+1:]
			except IndexError:
				num = num[:i] + left + right

		else:
			#no condition has been met - the snailfish number is reduced
			return num

def computeSum(num):
	#computes a magnitude sum of a snailfish number
	depths = list(range(1,5))
	depths.reverse()
	for d in depths:
		while d in [x[1] for x in num]:
			#sum the leftmost pair, replace with single number of 1 less depth
			#the sum is 3x the left value + 2x the right value
			i=0
			for x in num:
				if x[1] == d:
					break
				i+=1

			#i is index of leftmost deepest pair - replace this pair with a number equal to the sum, at 1 less depth
			z = (3*num[i][0]+2*num[i+1][0],d-1)
			#restructure list
			try:
				num = num[:i] + [z] + num[i+2:]
			except IndexError:
				num = num[:i] + [z]

	return num[0][0]

def part1():
	#add up all the snailfish numbers and reduce them after each addition
	data = readInput()

	num = reduce(flatten(data[0]))


	for num2 in data[1:]:
		#add num2 to existing number by forming another outside pair
		#flatten and reduce num2, then increase depths of both num and num2, and append num2 to num
		#one appended, reduce the existing number
		num = increaseDepth(num) + increaseDepth(reduce(flatten(num2)))
		num = reduce(num)

	#should have a final output here - now, compute the final sum - each pair is summed together recursisely to yield 1 number
	#a fully reduced number will not have any numbers at number-depth 5 - so we only need to work with depths 0-4 in reverse

	#now we should have a list with a single value in it
	print('The final answer is...{}'.format(computeSum(num)))

def part2():
	#find the largest possible magnitude sum of any 2 snailfish numbers in the input -- non-commutative
	data = readInput()

	permut = permutations(data,2)

	sums = []
	for pair in permut:
		num = reduce(increaseDepth(reduce(flatten(pair[0]))) + increaseDepth(reduce(flatten(pair[1]))))
		sums.append(computeSum(num))

	print('The maximum possible sum of 2 snailfish numbers from this input is...{}'.format(max(sums)))

if __name__ == "__main__":
	part1()
	part2()