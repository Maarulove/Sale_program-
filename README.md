# Pharmacy Management System

A complete pharmacy management system with graphical user interface for managing inventory, sales, and reports.

## Features

- Inventory management
- Sales tracking
- Monthly reports
- Automatic data backup
- User-friendly interface

## Requirements

- Python 3.x
- tkinter (usually comes with Python)

## Installation

1. Download and extract the ZIP file
2. Open Command Prompt or Terminal
3. Navigate to the program directory
4. Install requirements:
   ```
   pip install -r requirements.txt
   ```

## Running the Program

1. Double-click `run_pharmacy.bat` or
2. Open Command Prompt/Terminal and run:
   ```
   python pharmacy_gui.py
   ```

## Usage Guide

### Adding Products
1. Go to "Inventory" tab
2. Fill in the product details:
   - Code (unique identifier)
   - Name
   - Price
   - Quantity
3. Click "Add Product"

### Making Sales
1. Go to "Sales" tab
2. Enter product code and quantity
3. Click "Add to Cart"
4. Repeat for additional items
5. Click "Complete Sale"

### Viewing Reports
1. Go to "Reports" tab for daily sales
2. Go to "Monthly Reports" tab for monthly statistics
3. Select year and month to view historical data

## Data Storage

All data is automatically saved in the following locations:
- `data/products.json`: Product inventory
- `data/sales.json`: Sales records
- `data/monthly/`: Monthly reports
- `backups/`: Automatic backups
