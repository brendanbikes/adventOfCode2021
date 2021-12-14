from collections import Counter

def readInput():
	with open('./day14Input.txt', 'r') as f:
		data = [x.strip() for x in f.readlines()]

	polymer = [x for x in data[0]]

	rules = {}
	for row in data[2:]:
		pair, new = row.split(' -> ')
		rules[pair] = new

	return polymer, rules

def increment(counts, key, q):
	if not counts.get(key, 0):
		counts[key] = q
	else:
		counts[key] += q

	return counts

def part1():
	#brute force method
	polymer, rules = readInput()

	#number of times through the process
	N = 10

	for n in range(N):
		insertions = []
		for x in range(len(polymer)-1):
			pair = ''.join(polymer[x:x+2])

			new = rules.get(pair, '')	
			if new:
				insertions.append((x,new))

		#perform the insertions
		i = 0 #number of insertions performed
		for insertion in insertions:
			polymer = polymer[:insertion[0]+1+i] + [insertion[1]] + polymer[insertion[0]+1+i:]
			i+=1

		counts = {}
		for x in range(len(polymer)-1):
			pair = ''.join(polymer[x:x+2])

			if not counts.get(pair, 0):
				counts[pair]=1
			else:
				counts[pair]+=1

	letterCounts = {}
	for key, val in counts.items():
		for letter in key:
			if not letterCounts.get(letter, ''):
				letterCounts[letter] = val
			else:
				letterCounts[letter] += val

	#find most and least common elements
	counts = dict(Counter(polymer))

	print('The output is {}'.format(max([x for x in counts.values()]) - min([x for x in counts.values()])))

def part2():
	#optimize part 1 to handle really big numbers after more iterations
	polymer, rules = readInput()

	#number of times through the process
	N = 40

	#use different data structure -- count frequencies of pairs and letters
	counts = {}
	letters = {}

	for x in range(len(polymer)-1):
		pair = ''.join(polymer[x:x+2])
		if not counts.get(pair, 0):
			counts[pair]=1
		else:
			counts[pair]+=1

	for x in range(len(polymer)):
		if not letters.get(polymer[x],0):
			letters[polymer[x]] = 1
		else:
			letters[polymer[x]] +=1

	for n in range(N):
		newCounts = counts.copy()
		for key in counts.keys():
			q = counts[key]
			if q > 0:
				newCounts[key] -= q
				newCounts = increment(newCounts, key[0] + rules[key], q)
				newCounts = increment(newCounts, rules[key] + key[1], q)
				letters = increment(letters, rules[key], q)
		counts = newCounts.copy()

	print('The output is {}'.format(max([x for x in letters.values()]) - min([x for x in letters.values()])))

if __name__ == "__main__":
	part1()
	part2()