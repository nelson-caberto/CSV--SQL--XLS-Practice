import sqlite3

def createDBConnection(db_file=':memory:'):
	"""
	returns handle for accessing db as a file or by db_file default system memory	
	"""
	
	try:
		dbConnection = sqlite3.connect(db_file)
		return dbConnection
	except sqlite3.Error as e:
		print(e)
	except Exception as e:
		print(e)
	return None

if __name__ == '__main__':
	
### INIT DATABASE ###
	
	dbConnection = createDBConnection()
	
	if dbConnection is None:
		sys.exit('Failed to create dbConnection.')
	else:
		dbCursor = dbConnection.cursor()
		
	sqlSTMT = """
	CREATE TABLE IF NOT EXISTS employees (
		id integer PRIMARY KEY,
		int3 integer NOT NULL,
		char6 text NOT NULL,
		char2 text NOT NULL,
		int4a integer NOT NULL,
		float8 float NOT NULL,
		int4b integer NOT NULL );
	"""
	
	try:
		dbCursor.execute(sqlSTMT)
	except sqlite3.Error as e:
		sys.exit(f'Database Error: {e} on {sqlSTMT}')
	except Exception as e:
		sys.exit(f'Database Exception: {e} on {sqlSTMT}')


		
	dbCursor.close()