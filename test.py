ALPHA = 'abcdefghijklmnopqrstuvwxyz'

def funcASCII(c):
	return ALPHA.index(c)

def hashCode(item, numBins):
	hashCode = 0
	for i in item:
		hashCode = hashCode*31 + funcASCII(i)
	return hashCode % numBins

print(hashCode("nice", 5))