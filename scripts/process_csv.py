import csv
with open('toc.csv', newline='') as toc_csv:
  csv_data = csv.reader(toc_csv, delimiter=',')
  for row in csv_data:
    print(row)

