from itertools import product


steps = [12, 10, 8, 4, None, 10, 6, None, None, None, None, 6, None, None]
reqs = [None, None, None, None, 0, None, None, 12, 15, 15, 4, None, 5, 12]

#steps = [6, 12, 8, None, 7, 12, 2, None, 4, None, None, None, None, None]
#reqs = [None, None, None, 11, None, None, None, 7, None, 6, 10, 15, 9, 0]

#the steps array is the increments in z%26+increment, since we know that value can never equal w, so we just increment it
#the reqs array are the values in z%26-req=w, which needs to be true in order to proceed with checking a given number for validity
#the input space is the total set of predetermined numbers we need to iterate over -- these come into play on the steps where
#we do not have a requirement on the value of w in order to update the value of z and proceed, so we must iterate over all possible 1-9 digits
#for digits in those positions -- which is only half the entire problem space. The other half has restrictions.
#key idea is that we are building a number that fulfills these requirements, not checking whether a given 14-digit number meets the requirements
#We start the input space from the top at 9999999 to search for the largest such valid number, and at 1111111 to search for the lowest number


#thanks to womogenes at github.com/womogenes for the helpful walkthrough and sample code

def readInput():
	with open('./day24Input.txt', 'r') as f:
		data = [x.strip() for x in f.readlines()]

	print(data)

def checkDigits(digits):
	z=0 #begin - the starting z value doesn't matter at all, since we mod it by a small number repeatedly
	number = [0]*14
	digits_idx = 0

	for i in range(14):
		#need to run the 14 code blocks
		increment, mod_req = steps[i], reqs[i]

		if mod_req!=None:
			#we have a restriction on the value of w, because z%26-req = w
			#key idea -- we do not have a predetermined w here, so we are just setting w to z%26-req and then testing whether the w we computed is a digit between 1 and 9
			#if this w is not a digit between 1 and 9, we toss out this particular combination of the 7 predetermined digits and return, to try the next combination  
			w = ((z%26)-mod_req)
			if not (1<=w<=9):
				#the w we computed here based on the z, which has been determined from previous steps & predetermined digits, is not a valid 1-9 digit
				return False

			#else, file the number and update z
			number[i] = w
			z //=26 #update z as floor(z/26)

		else:
			#no requirement on w -- file the predetermined value from the chosen sequence, and increment z according to the increment rule z = 26*z+w+increment
			w = digits[digits_idx]
			z = 26*z + w + increment
			number[i] = w
			digits_idx+=1 #increment, but only as we use up the 7 predetermined digits from the sequence we took from the problem space

	return number

def part1():
	#find the largest number that satisfies the conditions
	input_space = product(range(9, 0, -1), repeat=7)

	for digits in input_space:
		number = checkDigits(digits)
		if number:
			print('Largest number found! It is {}'.format(''.join([str(x) for x in number])))
			break


def part2():
	#find the smallest such number that satisfies the conditions
	input_space = product(range(1,10), repeat=7)

	for digits in input_space:
		number = checkDigits(digits)
		if number:
			print('Smallest number found! It is {}'.format(''.join([str(x) for x in number])))
			break

if __name__ == "__main__":
	part1()
	part2()