import sys

def readInput():
	with open('./day17Input.txt', 'r') as f:
		data = [x.strip() for x in f.readlines()]

	data = data[0][13:]
	foo = []
	for x in data.split(', '):
		foo.append([int(y) for y in x[2:].split('..')])

	return foo

def fireProbe(x=0, y=0, vx=6, vy=9, xRange=[], yRange=[]):
	i=0
	h=0
	while True:
		if not(x in range(xRange[0],xRange[1]+1) and y in range(yRange[0],yRange[1]+1)):
			#iterate
			x+=vx
			newy = y+vy
			if newy > y:
				#update max height
				h = newy
			else:
				pass
			y+=vy

			#drag
			if vx>0:
				vx-=1
			elif x<0:
				vx+=1

			#gravity
			vy-=1

			i+=1
		else:
			#probe passes through target
			#print('Probe passes through target at coordinate (x,y) = {}'.format((x,y)))
			#print('The max height of this trajectory was {}'.format(h))
			return h

		if i > 1000:
			#probably too many steps
			#print('Overshot or undershot target area - try a different initial velocity trajectory')
			return None

def fireProbePart2(x=0, y=0, vx=6, vy=9, xRange=[], yRange=[]):
	i=0
	h=0
	while True:
		if not(x in range(xRange[0],xRange[1]+1) and y in range(yRange[0],yRange[1]+1)):
			#iterate
			x+=vx
			y+=vy

			#drag
			if vx>0:
				vx-=1
			elif x<0:
				vx+=1

			#gravity
			vy-=1

			i+=1
		else:
			#probe passes through target
			#print('Probe passes through target at coordinate (x,y) = {}'.format((x,y)))
			#print('The max height of this trajectory was {}'.format(h))
			return True

		if i > 1000:
			#probably too many steps
			#print('Overshot or undershot target area - try a different initial velocity trajectory')
			return False




def part1():
	xRange, yRange = readInput()

	#given an initial velocity trajectory of (x,y), does the probe pass through the range given by the input, at any point along its trajectory?
	#find the trajectory that yields maximum height at any point, while still hitting target

	#do a bunch of simulations and take the max height of them all
	heights = []
	h = 0
	r = range(max(xRange[1],abs(yRange[1])))

	#find a seed
	for vx in r:
		for vy in r:
			newh = fireProbe(vx=vx, vy=vy, xRange=xRange, yRange=yRange)
			if newh and newh>h:
				maxVx = vx
				maxVy = vy
				#heights.append(newh)
				h = newh

	print('Naive search yielded solution of vx {}, vy {}, with max height {}.'.format(maxVx, maxVy, h))

	#now, search for maximum-height trajectory smartly
	heights = []
	i=0
	vx = maxVx
	vy = maxVy
	print('init', vx, vy)
	while True:
		print(vx,vy)
		h = fireProbe(vx=vx, vy=vy, xRange=xRange, yRange=yRange)
		if h:
			heights.append(h)
			vy+=1

		else:
			vx-=1
			i+=1

		if i>10000 or vx<0:
			#probably tried enough, or solution won't work
			break

	maxHeight = max(heights)
	print(len(heights))

	print('The maximum possible height of all reasonable trajectories was {}'.format(maxHeight))

def part2():
	#exhaustive search of all valid trajectories
	xRange, yRange = readInput()

	heights = []
	n=0
	#this may need to be expanded
	z = max(xRange[1],abs(yRange[1]))+1
	rx = range(z)
	ry = range(yRange[0],2*z)

	valids=[]

	for vx in rx:
		for vy in range(yRange[0],z):
			print(vx,vy)
			foo = fireProbePart2(vx=vx, vy=vy, xRange=xRange, yRange=yRange)
			if foo:
				n+=1

	print('The number of valid trajectories is {}'.format(n))


if __name__ == "__main__":
	#part1()
	part2()