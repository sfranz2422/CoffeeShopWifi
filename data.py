import csv

class Get_Coffee_Data():
    def __init__(self):
        with open('cafe-data.csv', newline='') as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            list_of_rows = []
            for row in csv_data:
                list_of_rows.append(row)
        self.data = list_of_rows
