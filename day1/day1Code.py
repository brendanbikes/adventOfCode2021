import pandas as pd

def readInput():
	with open('./day1Input.txt', 'r') as f:
		data = f.readlines()

	return [int(x) for x in data]

def part1():
	data = readInput()
	m = len(data)

	i = 0
	n = 0
	while i < m-1:
		if data[i+1] > data[i]:
			n+=1

		i+=1

	print('The number of depth increases is {}.'.format(n))

	#other method using pandas

	df = pd.DataFrame([int(x) for x in data])
	diff = df.diff()
	n = len(diff.loc[diff[0]>0])

	print('The number of depth increases is {}.'.format(n))

def part2():
	#3-element sliding windows
	data = readInput()
	m = len(data)

	i = 0
	n=0

	windowSums=[]
	while i < m-3:
		if data[i+1] + data[i+2] + data[i+3] > data[i] + data[i+1] + data[i+2]:
			n+=1
		i+=1

	print('The number of depth increases is {}.'.format(n))


if __name__ == "__main__":
	#part1()
	part2()