
#this is the array of sums and frequencies for the rolling of 3 3-sided die, in (sum, freq) form. There are 27 possible combinations, but only 7 different possible sum outcomes
rf = [(3,1),(4,3),(5,6),(6,7),(7,6),(8,3),(9,1)]

def readInput():
	with open('./day21Input.txt', 'r') as f:
		data = [x.strip() for x in f.readlines()]

	return int(data[0][-1]), int(data[1][-1])


def wins(p1,t1,p2,t2,M=21):
	#this function counts the number of winning states for each player, given the current state of the game
	#when this function is called, the values in positions 3 and 4 above -- p2 and t2 -- were updated
	#p2,t2 contain information for the last active player
	#p1,t1 contain information for the current/next active player
	#active player information is fed into the right side of the input, and inactive player information is fed into the left side of the input
	#the right side of the input becomes the inactive player, and the left side of the input becomes the active player
	#in this way, this function switches which player is active on each consecutive round

	#test if the inactive player has won -- need to test before next iteration, because the inactive player is not about to make a move, and already made their move in the last round
	if t2 >= M: return (0,1) # p2 has won (never p1 since p1 about to move)

	#to update the current state of the active player, need to do (PlayerState + R)%10
	#to update the current score of the active player, 

	w1,w2 = 0,0
	for (r,f) in rf:

	    #c2 is active player win count
	    #c1 is inactive player win count
	    c2,c1 = wins(p2,t2,(p1+r)%10,t1+1+(p1+r)%10)
	    
	    #update win counts - w1 is active player, w2 is inactive player
	    w1,w2 = w1 + f * c1, w2 + f * c2

	#return win count for active player, inactive player
	return w1,w2

def process():
	p1,p2 = readInput()

	print("The bigger universe of wins is", max(wins(p1-1,0,p2-1,0))) #4,8 #6,7

if __name__ == "__main__":
	#redefine the point squares -- the old position 10 is now 9, such that when (position+roll) % 10 = 9, then score is increased by 9+1
	#and the old position 1 is now 0, such that when (position+roll) % 10 = 0, then score is increased by 0+1
	#this allows the score to be directly related to the (position+roll)%10
	#be careful with inputs -- when initial positions are 4,8, need to input 3 and 7 to this script
	
	process()