import sys
import numpy as np

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

def parsePacketsPart1(stream, packetTypeIDs=[], packetVersions=[], literals=[], versionSum=0, N=10000000, M=10000000000):
	#set N,M to some arbitrarily high value
	#num of parsed packets for this level
	#stream is the remaining stream left to parse
	m=0

	while len(stream) >= 11 and m <= M: #stream must at least contain 11 bits to be a valid packet - literal packets are the shortest possible
		version = int(stream[0:3],2)
		typeID = int(stream[3:6],2)
		packetVersions.append(version)
		packetTypeIDs.append(typeID)
		versionSum+=version
		m+=1

		if typeID == 4:
			#literal packet
			#get groups of 5 where first value is a 1, until a group of 5 prefixed by a 0 is reached
			f=1
			i=0
			numstr=''
			while f!=0:
				group = stream[i+6:i+11]
				f = int(group[0])
				numstr += group[1:]
				i+=5

			num = int(numstr,2)
			literals.append(num)

			#truncate stream
			stream = stream[6+(i):]
			#print('Stream is now reduced to {}'.format(len(stream)))

		else:
			#operator packet
			lengthTypeID = int(stream[6])
			if lengthTypeID == 0:
				#next 15 bits are a number that represents total length in bits of the sub-packets contained by this packet
				n = int(stream[7:7+15],2)
				print(stream[7+15:7+15+n])

				packetTypeIDs, packetVersions, literals, versionSum, junk, junk, M = parsePacketsPart1(stream[7+15:7+15+n], packetTypeIDs=packetTypeIDs, packetVersions=packetVersions, literals=[], versionSum=versionSum)
				stream = stream[7+15+n:]

			elif lengthTypeID == 1:
				#next 11 bits are a number that represents the number of sub-packets immmediately contained by this packet
				M = int(stream[7:7+11],2)

				packetTypeIDs, packetVersions, literals, versionSum, stream, junk, M = parsePacketsPart1(stream[7+11:], packetTypeIDs=packetTypeIDs, packetVersions=packetVersions, literals=[], versionSum=versionSum, M=M)

	return packetTypeIDs, packetVersions, literals, versionSum, stream, m, M


def parsePacketsPart2(stream, parentTypeID=-1, packetTypeIDs=[], packetVersions=[], literals=[], versionSum=0, N=10000000, M=10000000000):
	#set N,M to some arbitrarily high value
	#num of parsed packets for this level
	#stream is the remaining stream left to parse
	m=0
	v=0
	#literals=[]
	print('recur')
	print(literals)

	while len(stream) >= 11 and m <= M: #stream must at least contain 11 bits to be a valid packet - literal packets are the shortest possible
		version = int(stream[0:3],2)
		typeID = int(stream[3:6],2)
		packetVersions.append(version)
		packetTypeIDs.append(typeID)
		versionSum+=version
		print('\ntypeID', typeID)
		m+=1

		if typeID == 4:
			#literal packet
			print('\nliteral')
			#get groups of 5 where first value is a 1, until a group of 5 prefixed by a 0 is reached
			f=1
			i=0
			numstr=''
			while f!=0:
				group = stream[i+6:i+11]
				f = int(group[0])
				numstr += group[1:]
				i+=5

			num = int(numstr,2)
			literals.append(num)

			#truncate stream
			stream = stream[6+(i):]
			#print('Stream is now reduced to {}'.format(len(stream)))

		else:
			#operator packet
			print('\noperator')
			lengthTypeID = int(stream[6])
			#literals=[]
			print('next operator packet')
			print('literals', literals)
			if lengthTypeID == 0:
				#next 15 bits are a number that represents total length in bits of the sub-packets contained by this packet
				n = int(stream[7:7+15],2)
				print(stream[7+15:7+15+n])

				packetTypeIDs, packetVersions, v, versionSum, junk, junk, M = parsePacketsPart2(stream[7+15:7+15+n], parentTypeID=typeID, packetTypeIDs=packetTypeIDs, packetVersions=packetVersions, literals=[], versionSum=versionSum)
				stream = stream[7+15+n:]
				print('v1', v)
				literals.append(v)
				print('literals1', literals)

			elif lengthTypeID == 1:
				#next 11 bits are a number that represents the number of sub-packets immmediately contained by this packet
				M = int(stream[7:7+11],2)

				packetTypeIDs, packetVersions, v, versionSum, stream, junk, M = parsePacketsPart2(stream[7+11:], parentTypeID=typeID, packetTypeIDs=packetTypeIDs, packetVersions=packetVersions, literals=[], versionSum=versionSum, M=M)
				print(literals)
				print('v2', v)
				literals.append(v)
				print('literals2', literals)

	#evaluate the operator packet values

	print('\nevaluating the literals', literals)

	if parentTypeID == 0:
		print('test')
		v = sum(literals)
	elif parentTypeID == 1:
		v = np.product(literals)
	elif parentTypeID == 2:
		v = min(literals)
	elif parentTypeID == 3:
		v = max(literals)
	elif parentTypeID == 5:
		v = 1 if literals[0] > literals[1] else 0
	elif parentTypeID == 6:
		v = 1 if literals[0] < literals[1] else 0
	elif parentTypeID == 7:
		v = 1 if literals[0] == literals[1] else 0
	elif parentTypeID == -1:
		v = literals[0]

	print('v', v)
	print('returning literals', literals)

	return packetTypeIDs, packetVersions, v, versionSum, stream, m, M

def part1():
	#read in hexadecimal
	data = readInput()

	binary = ''
	for x in data:
		binary+=hexMap.get(x,'')


	print('Stream initial length is {}'.format(len(binary)))

	packetTypeIDs, packetVersions, literals, versionSum, stream, m, M = parsePacketsPart1(binary)

	print('\nVersion sum')
	print(versionSum)
	print('Packet Type IDs')
	print(packetTypeIDs)
	print('Packet versions')
	print(packetVersions)


def part2():
	data = readInput()

	data = '9C0141080250320F1802104A08'

	binary = ''
	for x in data:
		binary+=hexMap.get(x,'')

	packetTypeIDs, packetVersions, v, versionSum, stream, m, M = parsePacketsPart2(binary)

	print(packetTypeIDs)
	print(packetVersions)
	print(v)

if __name__ == "__main__":
	#part1()
	part2()