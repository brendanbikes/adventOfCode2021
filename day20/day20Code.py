import sys

def readInput():
	with open('./day20Input.txt', 'r') as f:
		data = f.readlines()

	algo = ''
	image = {}

	#find the break between the algorithm key and the image itself
	z=0
	for line in data:
		if line == '\n':
			break
		z+=1

	#the algorithm lines run through line i-1, including i-1, and the image is from i+1 to the end

	for line in data[:z]:
		algo+=line.strip()

	i=0
	for line in data[z+1:]:
		j=0
		for pixel in line.strip():
			image[(i,j)]=pixel
			j+=1
		i+=1

	return algo, image

def enlarge(image):
	#pad an image with dark pixels '.' and return it
	mmax = max([key[1] for key in image.keys()]) #num columns
	mmin = min([key[1] for key in image.keys()])
	nmax = max([key[0] for key in image.keys()]) #num rows
	nmin = min([key[0] for key in image.keys()])

	newImage = image.copy()

	#top and bottom borders
	for i in range(mmin-1,mmax+2):
		newImage[(nmin-1,i)] = '.'
		newImage[(nmax+1,i)] = '.'

	#left and right sides
	for i in range(nmin,nmax+1):
		newImage[(i,mmin-1)] = '.'
		newImage[(i,mmax+1)] = '.'

	return newImage

def enhance(image, algo, defaultPad='.'):
	#enhances an input image by applying the algorithm once and returns it
	newImage = image.copy()

	for i in sorted(list(set([x[0] for x in image.keys()]))):
		for j in sorted(list(set([x[1] for x in image.keys()]))):
			#get neighbors
			neighbors = image.get((i-1,j-1),defaultPad) + image.get((i-1,j),defaultPad) + image.get((i-1,j+1), defaultPad) + image.get((i,j-1),defaultPad) + image.get((i,j),defaultPad) + image.get((i,j+1),defaultPad) + image.get((i+1,j-1),defaultPad) + image.get((i+1,j), defaultPad) + image.get((i+1,j+1),defaultPad)

			#convert
			num = int(''.join([str(1) if x == '#' else str(0) for x in neighbors]),2)
			newImage[i,j] = algo[num]

	#trim the excess padding before return

	return newImage

def render(image):
	#render the current grid state

	for i in sorted(list(set([x[0] for x in image.keys()]))):
		row = []
		for j in sorted(list(set([x[1] for x in image.keys()]))):
			row.append(image.get((i,j)))
		print(''.join(row))

def process(image, algo, n):
	#process an image n times
	#step 1 is to increase the size of the image, padding with dark pixels, to allow for these new edge pixels -- which can interact with the existing image's pixels -- to be lit up
	#do the padding twice
	for i in range(n):
		image = enlarge(image)

	#step 2 is to calculate the lookup numbers for each pixel in the image and construct a new image
	for i in range(n):
		if i % 2 == 0:
			#even -- default last infinite pad value is .
			defaultPad = algo[int('111111111',2)]
		else:
			#odd -- default last infinite pad value is #
			defaultPad = algo[int('000000000',2)]
		image = enhance(image, algo, defaultPad=defaultPad)
		#render(image)

	return image

def part1():
	algo, image = readInput()

	n = 2 #number of times to do the process
	image = process(image, algo, n)

	#count the number of lit pixels
	print('The number of lit pixels is {}'.format(len([x for x in image.values() if x=='#'])))

def part2():
	#do enhancement 50 times
	algo, image = readInput()

	n = 50
	image = process(image, algo, n)
	#count the number of lit pixels
	print('The number of lit pixels is {}'.format(len([x for x in image.values() if x=='#'])))

if __name__ == "__main__":
	part1()
	part2()