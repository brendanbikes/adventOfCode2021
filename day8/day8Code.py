from itertools import permutations, product
import sys

def readInput():
	with open('./day8Input.txt', 'r') as f:
		data = f.readlines()

	rows = []
	for row in data:
		row = [x.strip().split(' ') for x in row.split('|')]
		rows.append(row)

	return rows


def permute(positions, letters):
	for x in positions:
		permut = permutations(x, len(letters))

		mappingsForThisDigit = []
		for comb in permut:
			zipped = zip(comb, letters)
			mappingsForThisDigit.append(zipped)

	return mappingsForThisDigit

def part1():
	data = readInput()

	#unique digits
	#digit 1 uses 2 segments
	#digit 4 uses 4 segments
	#digit 7 uses 3 segments
	#digit 8 uses all 7 segments
	#count digit displays of length 2, 3, 4, 7

	#non-unique digits
	#digit 0 uses 6 segments
	#digit 3 uses 5 segments
	#digit 5 uses 5 segments
	#digit 6 uses 6 segments
	#digit 9 uses 6 segments

	count = 0
	for signals, output in data:
		count += len([x for x in output if len(x) in (2, 3, 4, 7)])

	print('The number of 1, 4, 7, and 8 digits is {}.'.format(count))

def part2():
	data = readInput()

	#assign each segment in the digit display a consistent, unique ID
	# top segment - 0, label t
	# upper left - 1, label ul
	# upper right - 2, label ur
	# middle - 3, label m
	# lower left - 4, label ll
	# lower right - 5, label lr
	# bottom - 6, label b

	numbers = []
	total=0
	for signals, outputs in data:
		#find the unique mapping
		mappings = []
		decoded = False

		#deal with the unique signals first
		viableMappings = []
		for signal in signals:
			#print(signal)
			#split signal
			letters = [x for x in signal]
			if len(letters) == 2:
				#display digit is 1
				positions = ['ur', 'lr']

			elif len(letters) == 4:
				#display digit is 4
				positions = ['ul', 'ur', 'm', 'lr']

			elif len(letters) == 3:
				#display digit is 7
				positions = ['t', 'ur', 'lr']

			elif len(letters) == 7:
				#display digit is 8
				positions = ['t', 'ul', 'ur', 'm', 'll', 'lr', 'b']

			if len(letters) in (2, 3, 4, 7):
				permut = permutations(positions, len(letters))

				mappingsForThisDigit = []
				for comb in permut:
					zipped = zip(comb, letters)
					mappingsForThisDigit.append(set(list(zipped)))

				if len(viableMappings)==0:
					viableMappings = mappingsForThisDigit[:]
					#print(viableMappings)
				else:
					newViableMappings = []
					for x in viableMappings:
						for y in mappingsForThisDigit:
							#print(x,y)
							if x.issubset(y) or y.issubset(x):
								#one is wholly contained in the other - retain the larger as a viable mapping
								newViableMappings.append(x if len(x) > len(y) else y)

					if len(newViableMappings)>0:
						viableMappings = newViableMappings[:]

		#now deal with the non-unique digits
		for signal in signals:
			letters = [x for x in signal]
			if len(letters) == 5:
				#digit is 3 or 5 or 2
				positions = [['t', 'ur', 'm', 'lr', 'b'], ['t', 'ul', 'm', 'lr', 'b'], ['t', 'ur', 'm', 'll', 'b']]

			elif len(letters) == 6:
				#digit is 6 or 9 or 0
				positions = [['t', 'ul', 'm', 'll', 'lr', 'b'], ['t', 'ul', 'ur', 'm', 'lr', 'b'], ['ul', 't', 'ur', 'lr', 'b', 'll']]

			if len(letters) in (5,6):
				
				mappingsForThisDigit = []
				for z in positions:
					permut = permutations(z, len(letters))

					for comb in permut:
						zipped = zip(comb, letters)
						mappingsForThisDigit.append(set(list(zipped)))

				newViableMappings = []

				for x in viableMappings:
					for y in mappingsForThisDigit:
						if x.issubset(y) or y.issubset(x):
							newViableMappings.append(x if len(x) > len(y) else y)

				if len(newViableMappings)>0:
					viableMappings = newViableMappings[:]


		stop2=False
		for map in viableMappings:
			stop=False
			
			if stop2 == True:
				#don't continue with remaining maps -- already found right one
				break

			digits=[]
			for output in outputs:
				segments=set()
				for letter in output:
					#find first value of tuple corresponding to letter
					position = [x[0] for x in map if x[1]==letter][0]
					segments.add(position)


				if segments == {'ul', 't', 'ur', 'lr', 'b', 'll'}:
					#digit is 0
					digits.append(0)
				elif segments == {'ur', 'lr'}:
					#digit is 1
					digits.append(1)
				elif segments == {'t', 'ur', 'm', 'll', 'b'}:
					#digit is 2
					digits.append(2)
				elif segments == {'t', 'ur', 'm', 'lr', 'b'}:
					#digit is 3
					digits.append(3)
				elif segments == {'ul', 'ur', 'm', 'lr'}:
					#digit is 4
					digits.append(4)
				elif segments == {'t', 'ul', 'm', 'lr', 'b'}:
					#digit is 5
					digits.append(5)
				elif segments == {'t', 'ul', 'm', 'll', 'lr', 'b'}:
					#digit is 6
					digits.append(6)
				elif segments == {'t', 'ur', 'lr'}:
					#digit is 7
					digits.append(7)
				elif segments == {'t', 'ul', 'ur', 'm', 'll', 'lr', 'b'}:
					#digit is 8
					digits.append(8)
				elif segments == {'t', 'ul', 'ur', 'm', 'lr', 'b'}:
					#digit is 9
					digits.append(9)

				else:
					#print('incomplete map')
					stop=True
					break

			if stop is True:
				#skip to next map
				continue

			else:
				#construct number
				numstring = ''.join([str(x) for x in digits])
				num = int(numstring)
				total += num

				#need to stop to next set of signals
				stop2=True

	print('The total sum of numbers is {}'.format(total))

if __name__ == "__main__":
	part1()
	part2()