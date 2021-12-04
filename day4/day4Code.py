import re
import sys
import numpy as np

def readInput():
	with open('./day4Input.txt', 'r') as f:
		data = f.readlines()

	return [re.sub('  ', ' ', x.strip()) for x in data]

def wincon(board):
	rowsums = np.sum(board, axis=1)
	colsums = np.sum(board, axis=0)
	posSum = board.clip(min=0).sum()

	if -5 in rowsums or -5 in colsums:
		#board has a winning row or column- need to also return the sum of all positive numbers
		return True, posSum
	else:
		return False, 0

def part1():
	data = readInput()

	nums = [int(x) for x in data[0].split(',')]

	boardRows = []

	i=0
	boards=[]
	board=[]

	for row in data[1:]:
		if row == '':
			pass
		else:
			#add next row to current board
			row = [int(x) for x in row.split(' ')]
			board.append(row)

			if len(board) == 5:
				#board is finished
				boards.append(np.array(board))
				#start next board
				board = []

	k=0
	win = False

	while True:
		#pick next number and mark on the boards - set chosen numbers to -1
		#this way, checking for a win state is the same as checking if a row or column has a sum of -5

		newBoards=[]
		for board in boards:
			boardCopy = board[:]
			for i in range(0,5):
				for j in range(0,5):
					if board[i,j] == nums[k]:
						boardCopy[i][j] = -1

			#file back the board copy
			newBoards.append(boardCopy)

		#file all the boards
		boards = newBoards[:]
		#check the wincon for the current boards

		for board in boards:
			win, posSum = wincon(board)
			if win is True:
				#game over
				break

		if win is True:
			break

		k+=1

	#a board won, and the winning number is nums[k] and the board's sum is posSum

	print('A board won. The winning number is {}, the board has a sum of remaining numbers of {}, and the product is {}.'.format(nums[k], posSum, nums[k]*posSum))






def part2():
	#figure out the last board to win
	data = readInput()

	nums = [int(x) for x in data[0].split(',')]

	boardRows = []

	i=0
	boards=[]
	board=[]

	for row in data[1:]:
		if row == '':
			pass
		else:
			#add next row to current board
			row = [int(x) for x in row.split(' ')]
			board.append(row)

			if len(board) == 5:
				#board is finished
				boards.append(np.array(board))
				#start next board
				board = []

	k=0
	winBoards=[]

	while len(boards)>0:
		#pick next number and mark on the boards - set chosen numbers to -1
		#this way, checking for a win state is the same as checking if a row or column has a sum of -5
		#keep playing until only no boards remain - then the last board appended to winBoards is the last to win

		newBoards=[]
		for board in boards:
			boardCopy = board[:]
			for i in range(0,5):
				for j in range(0,5):
					if board[i,j] == nums[k]:
						boardCopy[i][j] = -1

			#file back the board copy
			newBoards.append(boardCopy)

		#file all the boards
		boards = newBoards[:]
		#check the wincon for the current boards

		newBoards=[]
		for board in boards:
			win, posSum = wincon(board)
			if win is True:
				#file away the winning board
				winBoards.append(board)
			else:
				#retain non-winning boards for future rounds
				newBoards.append(board)

		boards = newBoards[:]
		k+=1

	print('The last board has won. The winning number is {}, the board has a sum of remaining numbers of {}, and the product is {}.'.format(nums[k-1], posSum, nums[k-1]*posSum))



if __name__ == "__main__":
	#part1()
	part2()