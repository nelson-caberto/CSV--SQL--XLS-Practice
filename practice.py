import sqlite3
import sys
import csv

def createDBConnection(db_file):
	"""
	returns handle for accessing db as a file or in memory
	"""
	
	try:
		dbConnection = sqlite3.connect(db_file)
		return dbConnection
	except sqlite3.Error as e:
		print(e)
	except Exception as e:
		print(e)
	return None

def initializeDatabase(db_file=':memory:'):
	"""
	creates a new database or loads existing database
	"""

	dbConnection = createDBConnection(db_file)
	
	if dbConnection is None:
		sys.exit('Failed to create dbConnection.')
	else:
		dbCursor = dbConnection.cursor()
		
	sqlSTMT = """
	CREATE TABLE IF NOT EXISTS a (
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
	
	return dbConnection

def csvDBEntry(dbCursor, csv_file, sqlSTMT):
	with open(csv_file, mode='r') as file:
		csv_reader = csv.reader(file, delimiter=',')
		
		for row in csv_reader:
			try:
				dbCursor.execute(sqlSTMT, row)
			except sqlite3.Error as e:
				print(f'Database error: {e} on {row}')
				continue
			except Exception as e:
				print(f'Exception in _query: {e} on {row}')
				continue

if __name__ == '__main__':
	
### INIT DATABASE ###

	dbConnection = initializeDatabase()
	dbCursor = dbConnection.cursor()


### READ CSV's to DB ###

	csv_file = "input0.csv"

	sqlSTMT = """
	INSERT INTO a (
		id,
		int3,
		char6,
		char2,
		int4a,
		float8,
		int4b)
	VALUES (?,?,?,?,?,?,?);
	"""

	csvDBEntry(dbCursor, csv_file, sqlSTMT)	
	dbConnection.commit()
		
### COMPUTE ###

	char6s = ['A', 'B', 'C', 'D', 'E', 'F']
	char2s = ['A', 'B']
	float8s = [
		#[row, min, max],
		(7, 0, 19239),
		(8, 19240, 24439),
		(9, 24440, 30679),
		(10, 30680, 38999),
		(11, 39000, 49919),
		(12, 49920, 62919),
		(13, 62920, 80079),
		(14, 80080, 101919),
		(15, 101920, 128959),
		(16, 128960, 163799),
		(17, 163800, 207999),
		(18, 208000, sys.maxsize)
	]

	# Get a list possibilities of int4a in this dataset
	sqlSTMT = f'SELECT DISTINCT int4a FROM a;'
	try:
		dbCursor.execute(sqlSTMT)
	except sqlite3.Error as e:
		print(f'Database Error: {e} on {sqlSTMT}')
	except Exception as e:
		print(f'Exception in _query: {e} on {sqlSTMT}')
	int4as = [int4a[0] for int4a in dbCursor.fetchall()]
	int4as.sort()


	results = {}
	for int4a in int4as:
		results[int4a] = {}
		for char2 in char2s:
			results[int4a][char2] = {}
			for char6 in char6s:
				results[int4a][char2][char6] = {}
				for (row, min, max) in float8s:
					sqlSTMT = f'SELECT COUNT(*) FROM a WHERE int4a={int4a} AND char2="{char2}" AND char6="{char6}" AND float8 BETWEEN {min} AND {max}'
					try:
						dbCursor.execute(sqlSTMT)
					except sqlite3.Error as e:
						print(f"Database error: {e} on {sqlSTMT}")
						continue
					except Exception as e:
						print(f"Exception in _query: {e} on {sqlSTMT}")
						continue
					results[int4a][char2][char6][row] = dbCursor.fetchone()[0]

	totals = {}
	for (row, min, max) in float8s:
		sqlSTMT = f'SELECT COUNT(*) FROM a WHERE float8 BETWEEN {min} and {max}'
		try:
			dbCursor.execute(sqlSTMT)
		except sqlite3.Error as e:
			print(f'Database error: {e} on {sqlSTMT}')
			continue
		except Exception as e:
			print(f'Exception in _query: {e} on {sqlSTMT}')
			continue
		totals[row] = dbCursor.fetchone()[0]

	dbCursor.close()
	
### OUTPUT ###