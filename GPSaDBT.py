#!/usr/bin/python

import pycurl
import StringIO
import sys,getopt
import MySQLdb
import csv
import pdb
import sys
import readline
import glob

#---Constants---
consoleName = ['nes','super-nintendo','nintendo-64','gamecube','wii','wii-u','gameboy','gameboy-color','gameboy-advance','nintendo-ds','nintendo-3ds','virtual-boy','playstation',
'playstation-2','playstation-3','psp','playstation-vita','sega-master-system','sega-genesis','sega-cd','sega-32x','sega-saturn','sega-dreamcast','sega-game-gear','xbox','xbox-360'
,'atari-2600','atari-5200','atari-7800','atari-400','atari-lynx','jaguar','3do','cd-i','colecovision','commodore-64','intellivision','n-gage','neo-geo','neo-geo-pocket-color','odyssey-2'
'turbografx-16','vectrex','vic-20']

tableName = ['NES','SNES','N64','GAMECUBE','WII','WIIU','GAMEBOY','GAMEBOYC', 'GAMEBOYA','NDS','3DS','VIRTUALBOY','PS1','PS2','PS3','PSP','PSV','SMS','GENESIS','SEGACD','32X','SATURN','DREAMCAST','GAMEGEAR','XBOX','XBOX360',
'ATARI2600','ATARI5200','ATARI7200','ATARI400','ATARILYNX','ATARIJAGUAR','3DO','CDI','COLECO','C64','INTELLI','NGAGE','NEOGEO','NEOGEOP','ODYSSEY2','TURBOGRAFX16','VECTREX','VIC20']	
#---End Constants

#---Anon Functions---
def complete(text, state):
	return (glob.glob(text+'*')+[None])[state]
def commandLoop():
	readline.set_completer_delims(' \t\n;')
	readline.parse_and_bind("tab: complete")
	readline.set_completer(complete)
	
	input_line = ""
	while(True):
		input_line = raw_input(">")
		if input_line == "exit":
			break
		
		strings = input_line.split()
		if len(strings) < 3:
			print "Input too short"
			continue
			
		command = strings[0]
		arg1 = strings[1]
		arg2 = strings[2]
		
		
		if command == "search":
			if arg1 == "all":
				searchAll(arg2)
			else:
				try:
					cursor.execute('SELECT * FROM '+arg1+' WHERE Title LIKE "%'+arg2+'%";')
					rows = cursor.fetchall()
					for i in range(0,len(rows)):
						print rows[i]
				except:
					continue
		
		if command == "sum":
			
			gameType = ['Loose','New']
			index = 0 #Defaults to loose
			if arg2 == "-n":
				index = 1
			
			if arg1 == "all":
				sumAll(gameType[index])
			else:
				try:
					cursor.execute('SELECT SUM('+gameType[index]+') FROM '+arg1+';')
					rows = cursor.fetchall()
					for i in range(0,len(rows)):
						print rows[i]
				except:
					continue
					
		if command == "avg":
			gameType = ['Loose','New']
			index = 0 #Defaults to loose
			if arg2 == "-n":
				index = 1
			
			if arg1 == "all":
				avgAll(gameType[index])
			else:
				try:
					cursor.execute('SELECT AVG('+gameType[index]+') FROM '+arg1+';')
					rows = cursor.fetchall()
					for i in range(0,len(rows)):
						print rows[i]
				except:
					continue	
				
		if command == "add":
			if arg2 == "-c":
				fillUsingCSV(arg1)
			elif arg2 == "-t":
				fullUsingTXT(arg1)
			else:
				print "Invalid option: "+arg2	
				
		if command != "add" or command != "avg" or command != "search" or command != "sum":
			innerHelpInfo()
			
def helpInfo():
		print'''
				
		Usage: GPSaDBT [OPTIONS]
		
		-h, --help	Displays this help text and exits.
		-o 		Database host IP. If no IP is giving
				it is assumed localhost.
		-u		Database username. If no username is given
				Database connection can not be established.
				Unless username is logged in config file.
		-p		Database password. If no password is given.
				Database connection can not be established.
				Unless password is logged in config file.
		-d		Database name. If no name is given it is assumed
				the database name is GAMES. Unless name is 
				logged in config file.
		'''
		
#---End Anon Functions---

#---All Table Functions---
def searchAll(arg2):
	for arg1 in tableName:
		try:	
			cursor.execute('SELECT * FROM '+arg1+' WHERE Title LIKE "%'+arg2+'%";')
			rows = cursor.fetchall()
			for i in range(0,len(rows)):
				print arg1, rows[i]
		except:
			continue
def sumAll(gameType):
	for arg1 in tableName:
		try:	
			cursor.execute('SELECT SUM('+gameType+') FROM '+arg1+';')
			rows = cursor.fetchall()
			for i in range(0,len(rows)):
				print arg1, rows[i]
		except:
			continue
def avgAll(gameType):
	for arg1 in tableName:
		try:	
			cursor.execute('SELECT AVG('+gameType+') FROM '+arg1+';')
			rows = cursor.fetchall()
			for i in range(0,len(rows)):
				print arg1, rows[i]
		except:
			continue
#---END All Table Functions---

#---Initialization Functions---
def createTables():

	for name in tableName:
		tableCREATE = "CREATE TABLE "+name+"(Title varchar(100), Genre varchar(20), Loose double(7,2), New double(7,2));"  
		print tableCREATE
		cursor.execute(tableCREATE)

	db.commit()
def fillTables():
	
	for x in range(0,len(consoleName)):
		#Initial page
		c = pycurl.Curl()
		c.setopt(pycurl.URL, "http://videogames.pricecharting.com/console/"+consoleName[x]+"?sort-by=name")
		b = StringIO.StringIO()
		c.setopt(pycurl.WRITEFUNCTION, b.write)
		c.perform()
		c.close()
		data = b.getvalue()

		
		section= 0
		prevSection=section

		title = []#3 >'s away from "product id"
		genre = []#3 >'s away from title location
		loose = []#2 >'s away from genre
		new = []#2's >'s away from loose


		loopInc = 0 #used to determine when to get a new page. PriceCharting changes page every 30 entries in the table
		pageNum = 0
		while(data[section:].find("product-") + 8 != 7):# -1 no return status + 8
			#pdb.set_trace()
			section = data[section:].find("product-") +8
			section = prevSection+section
			prevSection = section
			
			arrowIndex=section#initial starting point
			prevIndex=arrowIndex
	
			#Finding titles
			for i in range(0,3):
				arrowIndex= data[arrowIndex:].find('>') + 1
				arrowIndex = arrowIndex+prevIndex
				arrowIndex = arrowIndex
				prevIndex = arrowIndex
			titleEnd = data[arrowIndex:].find('<')
			title.append(data[arrowIndex:arrowIndex+titleEnd])
	
			#Finding Genre
			for i in range(0,3):
				arrowIndex= data[arrowIndex:].find('>') + 1
				arrowIndex = arrowIndex+prevIndex
				arrowIndex = arrowIndex
				prevIndex = arrowIndex
			genreEnd = data[arrowIndex:].find('<')
			genre.append(data[arrowIndex:arrowIndex+genreEnd])
	
			#Finding Loose
			for i in range(0,2):
				arrowIndex= data[arrowIndex:].find('>') + 1
				arrowIndex = arrowIndex+prevIndex
				arrowIndex = arrowIndex
				prevIndex = arrowIndex
			looseEnd = data[arrowIndex:].find('<')
			loose.append(data[arrowIndex:arrowIndex+looseEnd])
	
			#Finding New
			for i in range(0,2):
				arrowIndex= data[arrowIndex:].find('>') + 1
				arrowIndex = arrowIndex+prevIndex
				arrowIndex = arrowIndex
				prevIndex = arrowIndex
			newEnd = data[arrowIndex:].find('<')
			new.append(data[arrowIndex:arrowIndex+newEnd])
	
			loopInc = loopInc + 1
			if loopInc != 0 and loopInc % 30 == 0:
				pageNum = pageNum + 1
				c = pycurl.Curl()
				c.setopt(pycurl.URL, "http://videogames.pricecharting.com/console/"+consoleName[x]+"?sort-by=name&page="+str(pageNum)+"&per-page=30")
				b = StringIO.StringIO()
				c.setopt(pycurl.WRITEFUNCTION, b.write)
				c.perform()
				c.close()
				data = b.getvalue()
				section = 0
				prevSection = 0
		
		genre = [w.replace('&amp;', '&') for w in genre]#Replacing substrings '&amp;' with just &
		loose = [w.replace('$','') for w in loose]# Removing $ dollar signs
		loose = [w.replace('none','0.0') for w in loose]# Replacing none string with 0
		loose = [str(w) for w in loose]
		loose = [float(w) for w in loose]
		new = [w.replace('$','') for w in new]
		new = [w.replace('none','0.0') for w in new]
		new = [str(w) for w in new]
		new = [float(w) for w in new]
		
		
		sqlDeleteRows = "DELETE FROM "+tableName[x]
		sqlTruncateRows = "TRUNCATE "+tableName[x]
		cursor.execute(sqlDeleteRows)
		cursor.execute(sqlTruncateRows)
		
		for j in range(0,len(title)):
			sqlInsert = "INSERT INTO "+tableName[x]+"(Title,Genre,Loose,New) VALUES ('" +MySQLdb.escape_string(title[j])+"',' "+genre[j]+"', '"+str(loose[j])+"', '"+str(new[j])+"')"
			cursor.execute(sqlInsert)
	
		db.commit()
	db.commit()
#---End Initialization Functions---


#---Adding Functions---
def fillUsingCSV(filepath):

	
	ifile = None
	
	try:
		ifile  = open(filepath, "rb")
	except:
		print filepath+" file not found"		
	
	partitions = filepath.split('/')
	name = partitions[-1]
	name = name[:-4]
	if name in tableName:
	
		try:
			cursor.execute("SELECT * FROM my"+name+";")
		except:
			cursor.execute("CREATE TABLE my"+name+"(Title varchar(100), Genre varchar(20), Loose double(7,2), New double(7,2));")  
		
		try:
			reader = csv.reader(ifile)
		except:
			print name+".csv file could not be read"
			sys.exit(1)
			
		myGames = []
		 
		rownum = 0
		for row in reader:
			# Save header row.
			colnum = 0
			for col in row:
				myGames.append(col)
				colnum += 1          
			rownum += 1
		 
		ifile.close()

		sqlDeleteRows = "DELETE FROM my"+name
		sqlTruncateRows = "TRUNCATE my"+name
		cursor.execute(sqlDeleteRows)
		cursor.execute(sqlTruncateRows)
		
		for i in range(0,len(myGames)):
			sqlInsert = "INSERT INTO my"+name+"(title) VALUES ('"+MySQLdb.escape_string(myGames[i])+"')"
			cursor.execute(sqlInsert)

		updateGenreCOL = "UPDATE my"+name+" SET genre = (SELECT genre FROM GAMECUBE WHERE my"+name+".title = "+name+".title);"
		updateLooseCOL = "UPDATE my"+name+" SET loose = (SELECT loose FROM GAMECUBE WHERE my"+name+".title = "+name+".title);"
		updateNewCOL = "UPDATE my"+name+" SET new = (SELECT new FROM GAMECUBE WHERE my"+name+".title = "+name+".title);"

		cursor.execute(updateGenreCOL)
		cursor.execute(updateLooseCOL)
		cursor.execute(updateNewCOL)

		db.commit()
		print "New table myGAMECUBE added succesfully"
	else:
		print "This is not a recognized table name"
# TODO: Add function for reading texts/ other formats other than CSV
#---End Adding Functions---


if __name__ == "__main__":
		
	try:
		opts, args = getopt.getopt(sys.argv[1:],"u:p:d:o:h:",["help"])
	except getopt.GetoptError, err:
		# print help information and exit:
		helpInfo()
		#print str(err) # will print something like "option -a not recognized"
		sys.exit(2)
		
	username = ""	
	password = "" 		
	database = ""
	host = ""
	#begin checking command line arguments
	for argName, argValue in opts:
		#help option
		if argName in ("-h", "--help"):
			helpInfo()
			sys.exit(1)
			
		if argName in ("-o"):
			host = argValue
		
		if argName in ("-u"):
			username = argValue
		
		if argName in ("-p"):
			password = argValue
			
		if argName in ("-d"):
			database = argValue

	if host == "" and database != "":
		try:
			db = MySQLdb.connect("localhost",username,password,database) 
			print "Connected to MYSQL database "+database+" at localhost"
		except:
			print "Could not connect to MYSQL database "+database+" at localhost"
			sys.exit(1)
	elif database == "" and host != "":
		try:
			db = MySQLdb.connect(host,username,password,"GAMES")
			print "Connected to MYSQL database GAMES at host: "+host  
		except:
			print "Could not connect to MYSQL database GAMES at host: "+host
			sys.exit(1)
	else:
		try:
			db = MySQLdb.connect("localhost",username,password,"GAMES")  
			print "Connected to MYSQL database GAMES at localhost"
		except:
			print "Could not connect to MYSQL database GAMES at localhost"
			sys.exit(1)
	
	cursor = db.cursor()
	
	commandLoop()
	
				
	db.close()
