

def readInput():
	with open('./day2Input.txt', 'r') as f:
		data = f.readlines()
		data = [(x.split(' ')[0], int(x.split(' ')[1])) for x in data]

	return data

def part1():
	data = readInput()

	x = 0 #initial horizontal position
	z = 0 #initial depth

	for command, value in data:
		if command == 'forward':
			x+=value

		elif command == 'down':
			z+=value

		elif command == 'up':
			z-=value

	print('The final x position is {}, and the final depth is {}. Their product is {}.'.format(x, z, x*z))


def part2():
	data = readInput()

	x = 0 #initial horizontal position
	z = 0 #initial depth
	p = 0 #initial pitch, or aim

	#forward X means forward that amount, but also change depth by that amount * the current aim

	for command, value in data:
		if command == 'forward':
			x+=value
			z+=p*value

		elif command == 'down':
			p+=value

		elif command == 'up':
			p-=value

	print('The final x position is {}, and the final depth is {}. Their product is {}.'.format(x, z, x*z))

if __name__ == "__main__":
	part1()
	part2()