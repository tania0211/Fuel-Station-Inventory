import csv
import os
from datetime import datetime

FUEL_FILE = r"c:\Users\tania\OneDrive\Desktop\FuelStationProject\fuel_data.csv"
SALES_FILE = r"c:\Users\tania\OneDrive\Desktop\FuelStationProject\sales_log.csv"

def read_fuel_data():
    fuel_quantities = {}
    if not os.path.exists(FUEL_FILE):
        print(f"{FUEL_FILE} not found!")
        return fuel_quantities
    with open(FUEL_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fuel_quantities[row['Fuel Type']] = float(row['Quantity (Liters)'])
    return fuel_quantities

def write_fuel_data(fuel_quantities):
    with open(FUEL_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Fuel Type', 'Quantity (Liters)'])
        for fuel_type, qty in fuel_quantities.items():
            writer.writerow([fuel_type, qty])
    print("Fuel data updated.")

def log_sale(fuel_type, quantity):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(SALES_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([now, fuel_type, quantity])
    print(f"Sale logged: {quantity} liters of {fuel_type} at {now}")

def check_fuel_levels(threshold=100):
    fuel_data = read_fuel_data()
    for fuel_type, qty in fuel_data.items():
        if qty < threshold:
            print(f"Warning: {fuel_type} level is low ({qty} liters). Please refill soon.")

def update_fuel(fuel_type, amount, is_sale=False):
    fuel_data = read_fuel_data()
    if fuel_type not in fuel_data:
        print(f"Fuel type '{fuel_type}' not found!")
        return

    fuel_data[fuel_type] += amount

    if fuel_data[fuel_type] < 0:
        print(f"Warning: Fuel quantity for {fuel_type} cannot be negative. Setting to 0.")
        fuel_data[fuel_type] = 0

    write_fuel_data(fuel_data)

    if is_sale:
        log_sale(fuel_type, -amount)  # Convert negative amount to positive for logging

    print(f"{fuel_type} quantity updated by {amount} liters.")
    check_fuel_levels()  # Check fuel levels after update

    from collections import defaultdict

from collections import defaultdict

def generate_daily_report():
    if not os.path.exists(SALES_FILE):
        print("No sales data available.")
        return

    daily_sales = defaultdict(lambda: defaultdict(float))  # {date: {fuel_type: total_qty}}

    with open(SALES_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 3:
                continue  # skip invalid rows
            timestamp, fuel_type, quantity = row
            date = timestamp.split(' ')[0]
            try:
                daily_sales[date][fuel_type] += float(quantity)
            except ValueError:
                print(f"Skipping invalid quantity: {quantity}")

    print("\n Daily Sales Report:")
    for date, fuels in sorted(daily_sales.items()):
        print(f"Date: {date}")
        for fuel_type, qty in fuels.items():
            print(f"  {fuel_type}: {qty:.2f} liters")
        print()


if __name__ == "__main__":
    while True:
        print("\n Fuel Station Management Menu:")
        print("1. View current fuel quantities")
        print("2. Refill fuel")
        print("3. Sell fuel")
        print("4. Show daily sales report")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            data = read_fuel_data()
            print("Current Fuel Quantities:")
            for fuel_type, qty in data.items():
                print(f"- {fuel_type}: {qty} liters")

        elif choice == '2':
            fuel = input("Enter fuel type to refill (Petrol/Diesel): ").capitalize()
            try:
                amount = float(input("Enter quantity to add (liters): "))
                update_fuel(fuel, amount)
            except ValueError:
                print("Invalid quantity.")

        elif choice == '3':
            fuel = input("Enter fuel type to sell (Petrol/Diesel): ").capitalize()
            try:
                amount = float(input("Enter quantity to sell (liters): "))
                update_fuel(fuel, -amount, is_sale=True)
            except ValueError:
                print("Invalid quantity.")
        
        elif choice == '4':
            generate_daily_report()

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
