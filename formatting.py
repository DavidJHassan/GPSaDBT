#---Table Printing---
def getFormatting(headers):
	spacing = []
	
	for i in range(0,len(headers)*18):
		if i % 18 == 0:
			spacing.append('|')
		else:
			spacing.append(' ')
	spacing.append('|')
	
	offset = 1
	for i in range(0,len(headers)):
		if i > 0:
			offset = 1-i
		for j in range(0,len(headers[i])):
			spacing[i*19+offset +j] = headers[i][j]
	
	line = []
	
	for i in range(0,len(headers)*18):
		if i % 18 == 0:
			line.append('|')
		else:
			line.append('-')
					
	line.append('|')		
			
	return ''.join(spacing), ''.join(line)

def printHeaders(headers):
	spacing,line = getFormatting(headers)
	print line
	print spacing
	print line
		
def printRow(cols):
	spacing,line = getFormatting(cols)
	
	print spacing
	print line
#---END Table printing---
