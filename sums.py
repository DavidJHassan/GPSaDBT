from formatting import *
from constants import *

def sums(cursor,gameType,arg1):
	if gameType == "Both":
		printHeaders(['Console','Loose','New'])
		cursor.execute('SELECT SUM(Loose), SUM(New) FROM '+arg1+';')
		rows = cursor.fetchall()
		printRow([arg1,str(rows[0][0]), str(rows[0][1])])
	else:
		printHeaders(['Console',gameType])
		cursor.execute('SELECT SUM('+gameType+') FROM '+arg1+';')
		rows = cursor.fetchall()
		printRow([arg1,str(rows[0][0])])
def sumAll(cursor,gameType):
	if gameType == "Both":
		printHeaders(['Console','Loose','New'])
		totalLoose = 0
		totalNew = 0
		for arg1 in tableName:
			try:	
				cursor.execute('SELECT SUM(Loose), SUM(New) FROM '+arg1+';')
				rows = cursor.fetchall()
				totalLoose = totalLoose + rows[0][0]
				totalNew = totalNew + rows[0][1]
				printRow([arg1,str(rows[0][0]), str(rows[0][1])])
			except:
				continue
				
		for arg1 in tableName:
			try:	
				cursor.execute('SELECT SUM(Loose), SUM(New) FROM my'+arg1+';')
				rows = cursor.fetchall()
				totalLoose = totalLoose + rows[0][0]
				totalNew = totalNew + rows[0][1]
				printRow(['my'+arg1,str(rows[0][0]), str(rows[0][1])])
			except:
				continue
		printRow(['TOTAL',str(totalLoose),str(totalNew)])
	else:
		printHeaders(['Console',gameType])
		totalLoose = 0
		for arg1 in tableName:
			try:	
				cursor.execute('SELECT SUM('+gameType+') FROM '+arg1+';')
				rows = cursor.fetchall()
				totalLoose = totalLoose + rows[0][0]
				printRow([arg1,str(rows[0][0])])
			except:
				continue
				
		for arg1 in tableName:
			try:	
				cursor.execute('SELECT SUM('+gameType+') FROM my'+arg1+';')
				rows = cursor.fetchall()
				totalLoose = totalLoose + rows[0][0]
				printRow(['my'+arg1,str(rows[0][0])])
			except:
				continue	
		printRow(['TOTAL',str(totalLoose)])	
def sumMY(cursor,gameType):
	if gameType == "Both":
		printHeaders(['Console','Loose','New'])
		totalLoose = 0
		totalNew = 0
		for arg1 in tableName:
			try:	
				cursor.execute('SELECT SUM(Loose), SUM(New) FROM my'+arg1+';')
				rows = cursor.fetchall()
				totalLoose = totalLoose + rows[0][0]
				totalNew = totalNew + rows[0][1]
				printRow(['my'+arg1,str(rows[0][0]), str(rows[0][1])])
			except:
				continue
				
		printRow(['TOTAL',str(totalLoose),str(totalNew)])
	else:
		printHeaders(['Console',gameType])
		totalLoose = 0
				
		for arg1 in tableName:
			try:	
				cursor.execute('SELECT SUM('+gameType+') FROM my'+arg1+';')
				rows = cursor.fetchall()
				totalLoose = totalLoose + rows[0][0]
				printRow(['my'+arg1,str(rows[0][0])])
			except:
				continue	
		printRow(['TOTAL',str(totalLoose)])		
def sumORIG(cursor,gameType):
	if gameType == "Both":
		printHeaders(['Console','Loose','New'])
		totalLoose = 0
		totalNew = 0
		for arg1 in tableName:
			try:	
				cursor.execute('SELECT SUM(Loose), SUM(New) FROM '+arg1+';')
				rows = cursor.fetchall()
				totalLoose = totalLoose + rows[0][0]
				totalNew = totalNew + rows[0][1]
				printRow([arg1,str(rows[0][0]), str(rows[0][1])])
			except:
				continue
				
		printRow(['TOTAL',str(totalLoose),str(totalNew)])
	else:
		printHeaders(['Console',gameType])
		totalLoose = 0
		for arg1 in tableName:
			try:	
				cursor.execute('SELECT SUM('+gameType+') FROM '+arg1+';')
				rows = cursor.fetchall()
				totalLoose = totalLoose + rows[0][0]
				printRow([arg1,str(rows[0][0])])
			except:
				continue
		printRow(['TOTAL',str(totalLoose)])
		
