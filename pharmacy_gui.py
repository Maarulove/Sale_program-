import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import calendar
import shutil
from pathlib import Path

class PharmacyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')

        # Initialize data
        self.products = {}
        self.sales = []
        self.monthly_data = {}
        self.current_month = datetime.now().strftime("%Y-%m")
        self.setup_data_directory()
        self.load_data()

        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        # Create tabs
        self.create_inventory_tab()
        self.create_sales_tab()
        self.create_reports_tab()
        self.create_monthly_reports_tab()

        # Style configuration
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 10))
        style.configure("TButton", padding=5, font=('Arial', 10))

        # Auto-save timer
        self.root.after(300000, self.auto_backup)  # Auto backup every 5 minutes

    def setup_data_directory(self):
        # Create directories for data organization
        Path("data").mkdir(exist_ok=True)
        Path("data/monthly").mkdir(exist_ok=True)
        Path("backups").mkdir(exist_ok=True)

    def load_data(self):
        # Load current data
        if os.path.exists('data/products.json'):
            with open('data/products.json', 'r') as f:
                self.products = json.load(f)
        
        if os.path.exists('data/sales.json'):
            with open('data/sales.json', 'r') as f:
                self.sales = json.load(f)

        # Load monthly data
        monthly_file = f'data/monthly/{self.current_month}.json'
        if os.path.exists(monthly_file):
            with open(monthly_file, 'r') as f:
                self.monthly_data = json.load(f)
        else:
            self.monthly_data = {
                'sales': [],
                'total_revenue': 0,
                'products_sold': {},
                'start_date': datetime.now().strftime("%Y-%m-%d")
            }

    def save_data(self):
        # Save current data
        with open('data/products.json', 'w') as f:
            json.dump(self.products, f, indent=4)
        
        with open('data/sales.json', 'w') as f:
            json.dump(self.sales, f, indent=4)

        # Save monthly data
        monthly_file = f'data/monthly/{self.current_month}.json'
        with open(monthly_file, 'w') as f:
            json.dump(self.monthly_data, f, indent=4)

    def auto_backup(self):
        # Create backup directory with timestamp
        backup_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"backups/backup_{backup_time}"
        os.makedirs(backup_dir, exist_ok=True)

        # Backup all data files
        shutil.copy2('data/products.json', f'{backup_dir}/products.json')
        shutil.copy2('data/sales.json', f'{backup_dir}/sales.json')
        
        # Backup monthly files
        for file in os.listdir('data/monthly'):
            shutil.copy2(f'data/monthly/{file}', f'{backup_dir}/{file}')

        # Schedule next backup
        self.root.after(300000, self.auto_backup)

    def create_inventory_tab(self):
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text='Inventory')

        # Product List
        tree_frame = ttk.Frame(inventory_frame)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.product_tree = ttk.Treeview(tree_frame, columns=('Code', 'Name', 'Price', 'Quantity'), show='headings')
        self.product_tree.heading('Code', text='Code')
        self.product_tree.heading('Name', text='Name')
        self.product_tree.heading('Price', text='Price')
        self.product_tree.heading('Quantity', text='Quantity')

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)

        self.product_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Add Product Form
        form_frame = ttk.LabelFrame(inventory_frame, text='Add New Product')
        form_frame.pack(pady=10, padx=10, fill='x')

        ttk.Label(form_frame, text='Code:').grid(row=0, column=0, padx=5, pady=5)
        self.code_entry = ttk.Entry(form_frame)
        self.code_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text='Name:').grid(row=0, column=2, padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text='Price:').grid(row=1, column=0, padx=5, pady=5)
        self.price_entry = ttk.Entry(form_frame)
        self.price_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text='Quantity:').grid(row=1, column=2, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(form_frame)
        self.quantity_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(form_frame, text='Add Product', command=self.add_product).grid(row=2, column=0, columnspan=4, pady=10)

        self.refresh_product_list()

    def create_sales_tab(self):
        sales_frame = ttk.Frame(self.notebook)
        self.notebook.add(sales_frame, text='Sales')

        # Cart
        cart_frame = ttk.LabelFrame(sales_frame, text='Shopping Cart')
        cart_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.cart_tree = ttk.Treeview(cart_frame, columns=('Code', 'Name', 'Price', 'Quantity', 'Total'), show='headings')
        self.cart_tree.heading('Code', text='Code')
        self.cart_tree.heading('Name', text='Name')
        self.cart_tree.heading('Price', text='Price')
        self.cart_tree.heading('Quantity', text='Quantity')
        self.cart_tree.heading('Total', text='Total')
        self.cart_tree.pack(pady=5, fill='both', expand=True)

        # Add to Cart Form
        form_frame = ttk.Frame(sales_frame)
        form_frame.pack(pady=10, padx=10, fill='x')

        ttk.Label(form_frame, text='Product Code:').pack(side='left', padx=5)
        self.sale_code_entry = ttk.Entry(form_frame)
        self.sale_code_entry.pack(side='left', padx=5)

        ttk.Label(form_frame, text='Quantity:').pack(side='left', padx=5)
        self.sale_quantity_entry = ttk.Entry(form_frame)
        self.sale_quantity_entry.pack(side='left', padx=5)

        ttk.Button(form_frame, text='Add to Cart', command=self.add_to_cart).pack(side='left', padx=5)
        ttk.Button(form_frame, text='Complete Sale', command=self.complete_sale).pack(side='left', padx=5)

    def create_reports_tab(self):
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text='Reports')

        # Sales Report
        report_frame = ttk.LabelFrame(reports_frame, text='Sales Report')
        report_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.sales_tree = ttk.Treeview(report_frame, columns=('Date', 'Items', 'Total'), show='headings')
        self.sales_tree.heading('Date', text='Date')
        self.sales_tree.heading('Items', text='Items')
        self.sales_tree.heading('Total', text='Total')
        self.sales_tree.pack(pady=5, fill='both', expand=True)

        self.refresh_sales_report()

    def create_monthly_reports_tab(self):
        monthly_frame = ttk.Frame(self.notebook)
        self.notebook.add(monthly_frame, text='Monthly Reports')

        # Month selector
        selector_frame = ttk.Frame(monthly_frame)
        selector_frame.pack(pady=5, padx=10, fill='x')

        years = sorted(set(file[:4] for file in os.listdir('data/monthly') if file.endswith('.json')))
        if not years:
            years = [datetime.now().strftime("%Y")]

        self.year_var = tk.StringVar(value=years[-1])
        self.month_var = tk.StringVar(value=datetime.now().strftime("%m"))

        ttk.Label(selector_frame, text="Year:").pack(side='left', padx=5)
        year_combo = ttk.Combobox(selector_frame, textvariable=self.year_var, values=years)
        year_combo.pack(side='left', padx=5)

        ttk.Label(selector_frame, text="Month:").pack(side='left', padx=5)
        month_combo = ttk.Combobox(selector_frame, textvariable=self.month_var, 
                                 values=[f"{i:02d}" for i in range(1, 13)])
        month_combo.pack(side='left', padx=5)

        ttk.Button(selector_frame, text="View Report", 
                  command=self.show_monthly_report).pack(side='left', padx=5)

        # Monthly statistics
        stats_frame = ttk.LabelFrame(monthly_frame, text='Monthly Statistics')
        stats_frame.pack(pady=5, padx=10, fill='both', expand=True)

        self.monthly_stats_tree = ttk.Treeview(stats_frame, 
                                             columns=('Metric', 'Value'),
                                             show='headings')
        self.monthly_stats_tree.heading('Metric', text='Metric')
        self.monthly_stats_tree.heading('Value', text='Value')
        self.monthly_stats_tree.pack(pady=5, fill='both', expand=True)

        # Top selling products
        top_products_frame = ttk.LabelFrame(monthly_frame, text='Top Selling Products')
        top_products_frame.pack(pady=5, padx=10, fill='both', expand=True)

        self.top_products_tree = ttk.Treeview(top_products_frame,
                                            columns=('Product', 'Quantity', 'Revenue'),
                                            show='headings')
        self.top_products_tree.heading('Product', text='Product')
        self.top_products_tree.heading('Quantity', text='Quantity Sold')
        self.top_products_tree.heading('Revenue', text='Revenue')
        self.top_products_tree.pack(pady=5, fill='both', expand=True)

    def show_monthly_report(self):
        selected_month = f"{self.year_var.get()}-{self.month_var.get()}"
        monthly_file = f'data/monthly/{selected_month}.json'

        if not os.path.exists(monthly_file):
            messagebox.showinfo("Info", "No data available for selected month")
            return

        with open(monthly_file, 'r') as f:
            data = json.load(f)

        # Clear existing data
        for item in self.monthly_stats_tree.get_children():
            self.monthly_stats_tree.delete(item)
        for item in self.top_products_tree.get_children():
            self.top_products_tree.delete(item)

        # Update statistics
        self.monthly_stats_tree.insert('', 'end', values=('Total Revenue', f"${data['total_revenue']:.2f}"))
        self.monthly_stats_tree.insert('', 'end', values=('Total Sales', len(data['sales'])))
        self.monthly_stats_tree.insert('', 'end', values=('Start Date', data['start_date']))
        
        # Update top products
        sorted_products = sorted(data['products_sold'].items(), 
                               key=lambda x: x[1]['revenue'], 
                               reverse=True)
        for product_code, stats in sorted_products[:10]:  # Show top 10
            product_name = self.products[product_code]['name']
            self.top_products_tree.insert('', 'end', values=(
                product_name,
                stats['quantity'],
                f"${stats['revenue']:.2f}"
            ))

    def add_product(self):
        try:
            code = self.code_entry.get()
            name = self.name_entry.get()
            price = float(self.price_entry.get())
            quantity = int(self.quantity_entry.get())

            if code in self.products:
                messagebox.showerror('Error', 'Product code already exists!')
                return

            if not all([code, name, price > 0, quantity >= 0]):
                messagebox.showerror('Error', 'Please fill all fields correctly!')
                return

            self.products[code] = {
                'name': name,
                'price': price,
                'quantity': quantity
            }

            self.save_data()
            self.refresh_product_list()
            self.clear_product_form()
            messagebox.showinfo('Success', f'Product "{name}" added successfully!')

        except ValueError:
            messagebox.showerror('Error', 'Invalid price or quantity!')

    def add_to_cart(self):
        code = self.sale_code_entry.get()
        try:
            quantity = int(self.sale_quantity_entry.get())
        except ValueError:
            messagebox.showerror('Error', 'Invalid quantity!')
            return

        if code not in self.products:
            messagebox.showerror('Error', 'Product not found!')
            return

        product = self.products[code]
        if quantity > product['quantity']:
            messagebox.showerror('Error', 'Insufficient stock!')
            return

        total = quantity * product['price']
        self.cart_tree.insert('', 'end', values=(code, product['name'], f"${product['price']:.2f}", quantity, f"${total:.2f}"))
        
        self.sale_code_entry.delete(0, 'end')
        self.sale_quantity_entry.delete(0, 'end')

    def complete_sale(self):
        if not self.cart_tree.get_children():
            messagebox.showerror('Error', 'Cart is empty!')
            return

        sale_items = []
        total_amount = 0

        for item in self.cart_tree.get_children():
            values = self.cart_tree.item(item)['values']
            code = values[0]
            quantity = int(values[3])
            amount = float(values[4].replace('$', ''))

            self.products[code]['quantity'] -= quantity
            sale_items.append({
                'code': code,
                'name': self.products[code]['name'],
                'quantity': quantity,
                'price': self.products[code]['price'],
                'amount': amount
            })
            total_amount += amount

            # Update monthly statistics
            if code not in self.monthly_data['products_sold']:
                self.monthly_data['products_sold'][code] = {
                    'quantity': 0,
                    'revenue': 0
                }
            self.monthly_data['products_sold'][code]['quantity'] += quantity
            self.monthly_data['products_sold'][code]['revenue'] += amount

        sale = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'items': sale_items,
            'total': total_amount
        }

        self.sales.append(sale)
        self.monthly_data['sales'].append(sale)
        self.monthly_data['total_revenue'] += total_amount

        self.save_data()
        self.refresh_product_list()
        self.refresh_sales_report()
        self.cart_tree.delete(*self.cart_tree.get_children())

        receipt = f"=== Receipt ===\nDate: {sale['date']}\n\nItems:\n"
        receipt += "Name\t\tQty\tPrice\tAmount\n"
        receipt += "-" * 40 + "\n"
        for item in sale_items:
            receipt += f"{item['name'][:12]}\t{item['quantity']}\t${item['price']:.2f}\t${item['amount']:.2f}\n"
        receipt += "-" * 40 + "\n"
        receipt += f"Total Amount: ${total_amount:.2f}"

        messagebox.showinfo('Sale Complete', receipt)

    def refresh_product_list(self):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)

        for code, product in self.products.items():
            self.product_tree.insert('', 'end', values=(
                code,
                product['name'],
                f"${product['price']:.2f}",
                product['quantity']
            ))

    def refresh_sales_report(self):
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)

        for sale in self.sales:
            items_str = f"{len(sale['items'])} items"
            self.sales_tree.insert('', 'end', values=(
                sale['date'],
                items_str,
                f"${sale['total']:.2f}"
            ))

    def clear_product_form(self):
        self.code_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')

def main():
    root = tk.Tk()
    app = PharmacyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 