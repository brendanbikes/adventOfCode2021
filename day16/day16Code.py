import sys

hexMap =  {
	'0': '0000',
	'1': '0001',
	'2': '0010',
	'3': '0011',
	'4': '0100',
	'5': '0101',
	'6': '0110',
	'7': '0111',
	'8': '1000',
	'9': '1001',
	'A': '1010',
	'B': '1011',
	'C': '1100',
	'D': '1101',
	'E': '1110',
	'F': '1111'
}

def readInput():
	with open('./day16Input.txt', 'r') as f:
		data = [x.strip() for x in f.readlines()]

	return data[0]

def parsePackets(stream, packets=[], versionSum=0, M=10000000000):
	#set M to some arbitrarily high value
	#num of parsed packets for this level
	m=0

	print('\nstarting parsing function')
	print(len(stream), m, M)
	print('length', len(stream))
	print('\n')

	while len(stream) >= 6 and m <= M: #stream must at least contain 7 bits to still be valid
		#thisPacket = stream[0:6]
		version = int(stream[0:3],2)
		typeID = int(stream[3:6],2)
		versionSum+=version
		print(version,typeID)

		if typeID == 4:
			#literal packet
			#get groups of 5 where first value is a 1, until a group of 5 prefixed by a 0 is reached
			print('literal')
			f=1
			i=0
			numstr=''
			while f!=0:
				group = stream[i+6:i+11]
				f = int(group[0])
				numstr += group[1:]
				i+=5

			num = int(numstr,2)
			packets.append(num)
			m+=1

			#truncate stream
			stream = stream[6+(i):]

		else:
			#operator packet
			print('operator')
			lengthTypeID = int(stream[6])

			if lengthTypeID == 0:
				#next 15 bits are a number that represents total length in bits of the sub-packets contained by this packet
				n = int(stream[7:7+15],2)
				m+=1
				print(stream[7+15:7+15+n])

				packets, versionSum, junk = parsePackets(stream[7+15:7+15+n], packets, versionSum)
				stream = stream[7+15+n:]

			elif lengthTypeID == 1:
				#next 11 bits are a number that represents the number of sub-packets immmediately contained by this packet
				M = int(stream[7:7+11],2)
				print('M', M)
				m+=1

				packets, versionSum, stream = parsePackets(stream[7+11:], packets, versionSum, M)

		print('end of while loop')
		print('\nlength', len(stream))


	#print('outside while loop')




	return packets, versionSum, stream





def part1():
	#read in hexadecimal
	data = readInput()

	binary = ''
	for x in data:
		binary+=hexMap.get(x,'')

	print(binary)

	packets, versionSum, stream = parsePackets(binary)

	print(packets, versionSum)


def part2():
	pass

if __name__ == "__main__":
	part1()
	part2()