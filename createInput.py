import argparse
import random
import sys
import csv

argvs = argparse.ArgumentParser(description='Create test input files.')
argvs.add_argument('lines', type=int, help='number of lines to generate')
argvs.add_argument('-f', type=int, default=1, help='number of files to generate')

if len(sys.argv) == 1:
	argvs.print_help()

args = argvs.parse_args()
lines = args.lines
files = args.f

char7 = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
char2 = ['A', 'B']

for count in range(0, files):
	with open('input_'+str(count)+'.csv', mode='w') as file:
		csv_file = csv.writer(file)
	
		headers = [
			'id',
			'int3',
			'char7',
			'char2',
			'int4a',
			'float8',
			'int4b',
		]
	
		csv_file.writerow(headers)
	
		for line in range(0, lines):
			
			data = [
				line,
				random.randrange(999),
				char7[random.randrange(7)],
				char2[random.randrange(2)],
				random.randrange(4),
				random.random()*10000*10**random.randrange(3),
				random.randrange(4)
			]
			
			csv_file.writerow(data)

