

def readInput():
	with open('./day21Input.txt', 'r') as f:
		data = [x.strip() for x in f.readlines()]

	return int(data[0][-1]), int(data[1][-1])

def newDieState(dieState):
	if dieState<100:
		dieState+=1
	else:
		dieState=1

	return dieState

def playerState(playerState,n):
	#calculate new player state based on sum of rolls n
	playerState = (playerState + n) % 10

	if playerState == 0:
		playerState = 10

	return playerState

def checkState(s1,s2):
	#check current state of game for win condition
	if s1>=1000 or s2>=1000:
		return True
	else:
		return False

def part1():
	p1, p2 = readInput()
	s1=0
	s2=0
	n=3 #number of die rolls
	dieState=0 #initial die state
	N=0 #total number of die rolls

	#deterministic practice game
	while True:
		#player 1's turn
		s=0
		for i in range(n):
			dieState = newDieState(dieState)
			s+=dieState
			N+=1

		#calculate player 1 score
		p1 = playerState(p1,s)
		s1+=p1

		if checkState(s1,s2):
			#player 1 won
			break

		#player 2's turn
		s=0
		for i in range(n):
			dieState = newDieState(dieState)
			s+=dieState
			N+=1

		#claculate player 2 score
		p2 = playerState(p2,s)
		s2+=p2

		if checkState(s1,s2):
			#player 2 won
			break

		#print current state of game
		#print('Player positions: {}, {}'.format(p1, p2))
		#print('Player scores: {}, {}'.format(s1, s2))

	#final state of game
	print('The final state of the game was Player 1: {}, Player 2: {}.'.format(s1,s2))

	print('The result is {}'.format(min([s1,s2])*N))


def part2():
	pass

if __name__ == "__main__":
	part1()
	part2()