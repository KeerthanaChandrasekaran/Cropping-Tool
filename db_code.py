import re
import pandas as pd
import csv
# read by default 1st sheet of an excel file
df = pd.read_excel('C:/Users/DELL/Desktop/Downloads/Test Data.xlsx',header=None)
print(type(df))
str=''
pattern = re.compile(r'(\d+) ([a-zA-Z ]+) ([a-zA-Z]+) ([a-zA-Z]+) ([a-zA-Z]+ [a-zA-Z]+?) (\d+@[a-z]+\.edu\.in) (\w+@[a-z]+\.com) ([A-Z]\.[a-zA-Z]+.*) (\d{1}) ([a-zA-Z]+) ([a-zA-Z]+) (\d{10}) (\d{4})')
for i in df.iloc[:,0]:
    str+=i
    str+='\n'
print(str)
match = pattern.findall(str)
print(match)
# with open('results.csv','w+',newline='') as out:
#     csv_out=csv.writer(out)
#     for row in match:
#         csv_out.writerow(row)




