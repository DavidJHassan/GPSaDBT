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
def innerHelpInfo():
	print'''
				
		Commands: 
		
		add [FileName.ext] [option] adds your game list to a table and updates it to have prices
				Ex: (add GAMECUBE.csv -c) adds csv list 
		
		search [Table] [String] searches a table for a title like the string
					Ex: (search GAMECUBE Zelda) returns all Zelda's in table GAMECUBE
					Ex: (search all Zelda) returns all Zelda's in all tables
			
		
		
		'''
