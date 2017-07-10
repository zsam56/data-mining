import csv
"""Decision Tree Program"""

def main():
	# convert the csv file to our list
	with open('HW_05B_DecTree_validation_data___v200.csv', 'r') as f:
		reader = csv.reader(f)
		data_list = list(reader)
	del data_list[0]

	output = open("HW_05_Samuelson_Zachary_MyClassifications.txt", "w")
	for item in data_list:
		if (float(item[1]) <= 7.87):
			if (float(item[3]) <= 5.01):
				output.write( str(1)+"\n")
			else: 
				if (float(item[1]) <= 4.94):
					output.write( str(0)+"\n")
				else: 
					output.write( str(1)+"\n")
		else: 
			output.write( str(0)+"\n")
	output.close()main()