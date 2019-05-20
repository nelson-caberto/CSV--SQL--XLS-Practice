import csv

with open('reduction.csv', 'r') as file:
	csv_reader = csv.reader(file, delimiter=',')
	data = []

	next(csv_reader)
	# row = next(csv_reader)
	# row.remove(row[0])
	
	for row in csv_reader:
		row.remove(row[0])
		s = ''
		for i in row:
			s += i
		print(int(s,2)&(1<<0)!=0)
	
	# s = ''
	# for i in row:
		# s += i

	# for row in csv_reader:
		# row.remove(row[0])
		# s = ''
		# for i in row:
			# s += i
		# h = "0x%x" % int(s,2)
		# print(type(h))

	""" to character """
	# a = []
	# while row:
		# bits = row[:8]
		# row = row[8:]
		# print(bits)
		# s = ''
		# for i in bits: s+=i
		# print(s)
		# c = chr(int(s,2))
		# print(c)
		# a.extend(c)
	# print(a)
		