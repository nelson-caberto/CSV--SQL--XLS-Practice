import csv

with open('meh.csv', 'w') as file:
	csv_file = csv.writer(file)
	data = []
	for col in range(1, 18):
		for row in range(1, 19):
			thing = str(col)+','+str(row)
			data.append(thing)
	csv_file.writerow(data)