import sqlite3
import sys
import csv

#pip install openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

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
		char7 text NOT NULL,
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
		char7,
		char2,
		int4a,
		float8,
		int4b)
	VALUES (?,?,?,?,?,?,?);
	"""

	csvDBEntry(dbCursor, csv_file, sqlSTMT)	
	dbConnection.commit()
		
### COMPUTE ###

	char6s = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
	char2s = ['A', 'B']
	float8s = [
		#[row, min, max],
		(7, 0, 19999),
		(8, 20000, 24999),
		(9, 25000, 30999),
		(10, 31000, 39999),
		(11, 40000, 49999),
		(12, 50000, 69999),
		(13, 70000, 99999),
		(14, 100000, 109999),
		(15, 110000, 129999),
		(16, 130000, 169999),
		(17, 170000, 209999),
		(18, 210000, sys.maxsize)
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
			for char7 in char6s:
				results[int4a][char2][char7] = {}
				for (row, min, max) in float8s:
					sqlSTMT = f'SELECT COUNT(*) FROM a WHERE int4a={int4a} AND char2="{char2}" AND char7="{char7}" AND float8 BETWEEN {min} AND {max}'
					try:
						dbCursor.execute(sqlSTMT)
					except sqlite3.Error as e:
						print(f"Database error: {e} on {sqlSTMT}")
						continue
					except Exception as e:
						print(f"Exception in _query: {e} on {sqlSTMT}")
						continue
					results[int4a][char2][char7][row] = dbCursor.fetchone()[0]

	totals = {}
	for int4a in int4as:
		totals[int4a] = {}
		for (row, min, max) in float8s:
			sqlSTMT = f'SELECT COUNT(*) FROM a WHERE int4a={int4a} AND float8 BETWEEN {min} and {max};'
			try:
				dbCursor.execute(sqlSTMT)
			except sqlite3.Error as e:
				print(f'Database error: {e} on {sqlSTMT}')
				continue
			except Exception as e:
				print(f'Exception in _query: {e} on {sqlSTMT}')
				continue
			totals[int4a][row] = dbCursor.fetchone()[0]

	dbCursor.close()
	
### OUTPUT ###

wb = Workbook()
ws = wb.active
offset = 0

cell = lambda column, row: get_column_letter(column+offset)+str(row)

for int4a in int4as:

	#A
	ws[cell(1,5)] = 'int4a'
	ws[cell(1,7)] = f'{int4a}'

	#B
	ws[cell(2,5)] = 'float8'
	ws[cell(2,7)] = f'{float8s[0][2]} and under'
	ws[cell(2,8)] = f'{float8s[1][1]} - {float8s[1][2]}'
	ws[cell(2,9)] = f'{float8s[2][1]} - {float8s[2][2]}'
	ws[cell(2,10)] = f'{float8s[3][1]} - {float8s[3][2]}'
	ws[cell(2,11)] = f'{float8s[4][1]} - {float8s[4][2]}'
	ws[cell(2,12)] = f'{float8s[5][1]} - {float8s[5][2]}'
	ws[cell(2,13)] = f'{float8s[6][1]} - {float8s[6][2]}'
	ws[cell(2,14)] = f'{float8s[7][1]} - {float8s[7][2]}'
	ws[cell(2,15)] = f'{float8s[8][1]} - {float8s[8][2]}'
	ws[cell(2,16)] = f'{float8s[9][1]} - {float8s[9][2]}'
	ws[cell(2,17)] = f'{float8s[10][1]} - {float8s[10][2]}'
	ws[cell(2,18)] = f'{float8s[11][1]} and over'

	#C
	ws[cell(3,1)] = 'Title'
	ws[cell(3,2)] = 'char7'
	ws[cell(3,3)] = 'char7[0]'
	ws[cell(3,5)] = 'char2[0]'
	ws[cell(3,6)] = 'A'
	result = results[int4a]['A']['A']
	for row in result: ws[cell(3,row)] = result[row]

	#D
	ws[cell(4,5)] = 'char2[1]'
	ws[cell(4,6)] = 'B'
	result = results[int4a]['B']['A']
	for row in result: ws[cell(4,row)] = result[row]

	#E
	ws[cell(5,3)] = 'Non/char7[0]'
	ws[cell(5,4)] = 'char2[0]'
	ws[cell(5,5)] = 'char7[1]'
	ws[cell(5,6)] = 'C'
	result = results[int4a]['A']['B']
	for row in result: ws[cell(5,row)] = result[row]

	#F
	ws[cell(6,5)] = 'char7[2]'
	ws[cell(6,6)] = 'D'
	result = results[int4a]['A']['C']
	for row in result: ws[cell(6,row)] = result[row]

	#G
	ws[cell(7,5)] = 'char7[3]'
	ws[cell(7,6)] = 'E'
	result = results[int4a]['A']['D']
	for row in result: ws[cell(7,row)] = result[row]

	#H
	ws[cell(8,5)] = 'char7[4]'
	ws[cell(8,6)] = 'F'
	result = results[int4a]['A']['E']
	for row in result: ws[cell(8,row)] = result[row]

	#I
	ws[cell(9,5)] = 'char7[5]'
	ws[cell(9,6)] = 'G'
	result = results[int4a]['A']['F']
	for row in result: ws[cell(9,row)] = result[row]

	#J
	ws[cell(10,5)] = 'char7[6]'
	ws[cell(10,6)] = 'H'
	result = results[int4a]['A']['G']
	for row in result: ws[cell(10,row)] = result[row]

	#K
	ws[cell(11,4)] = 'char2[1]'
	ws[cell(11,5)] = 'char7[1]'
	ws[cell(11,6)] = 'I'
	result = results[int4a]['B']['B']
	for row in result: ws[cell(11,row)] = result[row]

	#L
	ws[cell(12,5)] = 'char7[2]'
	ws[cell(12,6)] = 'J'
	result = results[int4a]['B']['C']
	for row in result: ws[cell(12,row)] = result[row]

	#M
	ws[cell(13,5)] = 'char7[3]'
	ws[cell(13,6)] = 'K'
	result = results[int4a]['B']['D']
	for row in result: ws[cell(13,row)] = result[row]

	#N
	ws[cell(14,5)] = 'char7[4]'
	ws[cell(14,6)] = 'L'
	result = results[int4a]['B']['E']
	for row in result: ws[cell(14,row)] = result[row]

	#O
	ws[cell(15,5)] = 'char7[5]'
	ws[cell(15,6)] = 'M'
	result = results[int4a]['B']['F']
	for row in result: ws[cell(15,row)] = result[row]

	#P
	ws[cell(16,5)] = 'char7[6]'
	ws[cell(16,6)] = 'N'
	result = results[int4a]['B']['G']
	for row in result: ws[cell(16,row)] = result[row]

	#Q
	ws[cell(17,5)] = 'Total Col A-N'
	ws[cell(17,6)] = 'O'
	total = totals[int4a]
	for row in total: ws[cell(17,row)] = total[row]
	
	offset += 17

wb.save("output0.xlsx")
