import os
import json
from datetime import datetime

class PharmacySystem:
    def __init__(self):
        self.products = {}
        self.sales = []
        self.load_data()

    def load_data(self):
        # Load products from file if exists
        if os.path.exists('products.json'):
            with open('products.json', 'r') as f:
                self.products = json.load(f)
        
        # Load sales from file if exists
        if os.path.exists('sales.json'):
            with open('sales.json', 'r') as f:
                self.sales = json.load(f)

    def save_data(self):
        # Save products to file
        with open('products.json', 'w') as f:
            json.dump(self.products, f, indent=4)
        
        # Save sales to file
        with open('sales.json', 'w') as f:
            json.dump(self.sales, f, indent=4)

    def add_product(self):
        print("\n=== Add New Product ===")
        code = input("Enter product code: ")
        if code in self.products:
            print("Product already exists!")
            return
        
        name = input("Enter product name: ")
        try:
            price = float(input("Enter product price: "))
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid input! Price and quantity must be numbers.")
            return

        self.products[code] = {
            "name": name,
            "price": price,
            "quantity": quantity
        }
        self.save_data()
        print(f"\nProduct '{name}' added successfully!")

    def view_products(self):
        print("\n=== Product List ===")
        print("Code\tName\t\tPrice\tQuantity")
        print("-" * 40)
        for code, product in self.products.items():
            print(f"{code}\t{product['name'][:12]}\t${product['price']:.2f}\t{product['quantity']}")

    def make_sale(self):
        print("\n=== New Sale ===")
        sale_items = []
        total_amount = 0

        while True:
            self.view_products()
            code = input("\nEnter product code (or 'done' to finish): ")
            
            if code.lower() == 'done':
                break

            if code not in self.products:
                print("Product not found!")
                continue

            try:
                quantity = int(input("Enter quantity: "))
            except ValueError:
                print("Invalid quantity!")
                continue

            if quantity > self.products[code]['quantity']:
                print("Insufficient stock!")
                continue

            product = self.products[code]
            amount = quantity * product['price']
            
            sale_items.append({
                "code": code,
                "name": product['name'],
                "quantity": quantity,
                "price": product['price'],
                "amount": amount
            })

            # Update stock
            self.products[code]['quantity'] -= quantity
            total_amount += amount

        if sale_items:
            # Record the sale
            sale = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "items": sale_items,
                "total": total_amount
            }
            self.sales.append(sale)
            self.save_data()

            # Print receipt
            print("\n=== Receipt ===")
            print("Date:", sale["date"])
            print("\nItems:")
            print("Name\t\tQty\tPrice\tAmount")
            print("-" * 40)
            for item in sale_items:
                print(f"{item['name'][:12]}\t{item['quantity']}\t${item['price']:.2f}\t${item['amount']:.2f}")
            print("-" * 40)
            print(f"Total Amount: ${total_amount:.2f}")

    def check_stock(self):
        print("\n=== Low Stock Alert ===")
        print("Products with quantity less than 10:")
        print("Code\tName\t\tQuantity")
        print("-" * 40)
        for code, product in self.products.items():
            if product['quantity'] < 10:
                print(f"{code}\t{product['name'][:12]}\t{product['quantity']}")

    def view_sales_report(self):
        print("\n=== Sales Report ===")
        if not self.sales:
            print("No sales recorded yet!")
            return

        total_sales = sum(sale['total'] for sale in self.sales)
        print(f"Total Sales: ${total_sales:.2f}")
        print(f"Number of Transactions: {len(self.sales)}")

def main():
    system = PharmacySystem()
    
    while True:
        print("\n=== Pharmacy Management System ===")
        print("1. Add New Product")
        print("2. View Products")
        print("3. Make Sale")
        print("4. Check Stock")
        print("5. View Sales Report")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            system.add_product()
        elif choice == '2':
            system.view_products()
        elif choice == '3':
            system.make_sale()
        elif choice == '4':
            system.check_stock()
        elif choice == '5':
            system.view_sales_report()
        elif choice == '6':
            print("\nThank you for using Pharmacy Management System!")
            break
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main() 