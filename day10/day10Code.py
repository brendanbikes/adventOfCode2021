from math import ceil


#global stuff

openChars = ['(', '[', '{', '<']

forward = {'(' : ')',
		'{' : '}',
		'[': ']',
		'<': '>'
		}

points = {')' : 3,
		']': 57,
		'}': 1197,
		'>': 25137
		}

closePoints = {')': 1,
				']': 2,
				'}': 3,
				'>': 4
				}

def readInput():
	with open('./day10Input.txt', 'r') as f:
		data = f.readlines()

	return [x.strip() for x in data]

def part1():
	#check for illegal syntax
	# illegal ) is 3 points
	# illegal ] is 57 points
	# illegal } is 1197 points
	# illegal > is 25137 points

	#after any opening character e.g. (,  the legal characters are:
		# ), to close
		# any new opening

	#after any closing character e.g. ), the legal characters are:
		# any new opening
		# closing the most recent opening that is still open, which may be a ways back

	#keep an ordered list of currently open pairs, and delete from it from the right when an interval is close

	data = readInput()

	score=0

	validLines = []
	for line in data:
		openings = []
		closings = [] #not sure if will need?

		valid=True
		for char in line:
			if char in openChars:
				#append to openings
				openings.append(char)
			elif char == forward[openings[-1]]:
				#closing character matches most recent open character in openings list
				#remove most recent opening character, since its interval is now closed
				openings = openings[:-1]

			else:
				#illegal character encountered
				print('Illegal character encountered! It is {}, worth {} points.'.format(char, points[char]))
				score+=points[char]

				valid = False
				break

		if valid == True:
			#valid but incomplete line -- save it
			validLines.append(line)


	print('The total score of illegal characters is {}.'.format(score))

	return validLines

def part2():
	validLines = part1()

	#determine the needed sequences to complete each incomplete line

	scores=[]
	for line in validLines:
		score=0
		openings = []
		for char in line:
			if char in openChars:
				#append to openings
				openings.append(char)
			elif char == forward[openings[-1]]:
				openings = openings[:-1]

		#now, the remaining openings need to be completed, in reverse order

		openings.reverse()
		closings = []
		for char in openings:
			closeChar = forward[char]
			score *= 5
			score += closePoints[closeChar]
		scores.append(score)

	#sort and find the middle score

	scores.sort()

	print('The final score is {}'.format(scores[int(ceil(len(scores)/2))]))

if __name__ == "__main__":
	#part1()
	part2()