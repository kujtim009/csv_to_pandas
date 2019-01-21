import pandas
import csv


csv_data = pandas.read_csv("sample_file/100K_sample.csv", encoding = "latin1", engine='python')

# myData = csv_file.group_by('City')
myData = csv_data.drop_duplicates(subset = "co_name1" , inplace = True)
print(myData)