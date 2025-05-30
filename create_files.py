<<<<<<< HEAD
import csv
import os


def create_csv_file(filename, header, rows=[]):
    print(f"Checking for file: {filename}")
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in rows:
                writer.writerow(row)
        print(f"{filename} created successfully.")
    else:
        print(f"{filename} already exists.")

folder = r"c:\Users\tania\OneDrive\Desktop\FuelStationProject"

create_csv_file(os.path.join(folder, 'fuel_data.csv'), ['Fuel Type', 'Quantity (Liters)'], [['Petrol', 0], ['Diesel', 0]])
create_csv_file(os.path.join(folder, 'sales_log.csv'), ['Date', 'Fuel Type', 'Quantity Sold (Liters)'])
create_csv_file(os.path.join(folder, 'issues_log.csv'), ['Date', 'Issue Description'])


=======
import csv
import os


def create_csv_file(filename, header, rows=[]):
    print(f"Checking for file: {filename}")
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in rows:
                writer.writerow(row)
        print(f"{filename} created successfully.")
    else:
        print(f"{filename} already exists.")

folder = r"c:\Users\tania\OneDrive\Desktop\FuelStationProject"

create_csv_file(os.path.join(folder, 'fuel_data.csv'), ['Fuel Type', 'Quantity (Liters)'], [['Petrol', 0], ['Diesel', 0]])
create_csv_file(os.path.join(folder, 'sales_log.csv'), ['Date', 'Fuel Type', 'Quantity Sold (Liters)'])
create_csv_file(os.path.join(folder, 'issues_log.csv'), ['Date', 'Issue Description'])


>>>>>>> e56aad4d530c64130dce55202669a57242cbb318
