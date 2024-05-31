import csv

filename = 'books.csv'
fields = ['Title', 'Price', 'Description', 'Page']

def add_header():
    with open(filename, 'a') as csvfile:
      csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
      csvwriter.writeheader()

def append_row(row):
    with open(filename, 'a') as csvfile:
      csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
      csvwriter.writerow(row)
