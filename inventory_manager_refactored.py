import os
import json
from pathlib import Path
from inventory import Inventory
from product import PhysicalProduct, DigitalProduct

def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False
    
def validate_str_input(user_input):
    if user_input.isdigit() or user_input.strip() == '':
        print("Error! Please enter a string value!")
        return None
    return user_input

def validate_int_input(user_input):
    if user_input.isdigit() and int(user_input) > 0:
        return int(user_input)
    print("Error! Please enter a positive integer!")
    return None

def validate_float_input(user_input):
    if is_float(user_input) and float(user_input) > 0:
        return float(user_input)
    print("Error! Please enter a positive float value!")
    return None
    
def load_inventory(file_path):
    inventory_obj = Inventory()
    if os.path.exists(file_path):
        if os.path.getsize(file_path) != 0:
            try:
                with open(file_path, 'r', encoding="utf-8") as file:
                    content = json.load(file)
                    for item in content:
                        raw_price = item['Price'].replace('$', '') if isinstance(item['Price'], str) else item['Price']
                        product_type = item.get('Type', 'Physical')
                        
                        if product_type == 'Physical':
                            weight = float(item.get('Weight', 1.0)) 
                            product = PhysicalProduct(item['ID'], item['Name'], float(raw_price), item['Stock'], weight)
                        elif product_type == 'Digital':
                            download_size = float(item.get('DownloadSize', 100.0))
                            product = DigitalProduct(item['ID'], item['Name'], float(raw_price), item['Stock'], download_size)
                            
                        inventory_obj._products.append(product) 
            except json.JSONDecodeError:
                pass
    else:
        with open(file_path, 'x', encoding="utf-8") as file:
            pass
    return inventory_obj

def save_inventory(file_path, inventory_obj, menu_option):
    inv_list = [product.to_dict() for product in inventory_obj.get_all_products()]
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(inv_list, file, indent=4)
    
    if menu_option == '5':
        print(f'\nSaving inventory...\nInventory saved to {file_path}')
    else:
        print('\nSaving inventory before exit...Inventory saved successfully.')


file = Path('inventory.json')
inventory = load_inventory(file)

print('''
========================================
INVENTORY MANAGEMENT SYSTEM
========================================
''')

if not inventory.get_all_products():
    print(f'{file} either not found, is empty or is in an invalid format.')
else:
    print(f'{file} found.\nInventory loaded successfully.\n')

while True:
    print('''
----------- MENU -----------
1. Display All Products
2. Add Product
3. Update Stock
4. Search Product
5. Save Inventory
6. Exit
----------------------------
''')
    option = input("\nEnter option: ")
    match option:
        case '1':
            inventory.display_all()
        case '2':
            print('Add New Product')
            p_type = input('Enter Product Type (1 for Physical, 2 for Digital): ')
            if p_type not in ['1', '2']:
                print("Invalid product type selected.")
                continue
                
            product_id = validate_str_input(input('Product ID: '))
            product_name = validate_str_input(input('Product Name: '))
            product_price = validate_float_input(input('Price: '))
            product_stock = validate_int_input(input('Stock Quantity: '))
            
            if all(v is not None for v in [product_id, product_name, product_price, product_stock]):
                if p_type == '1':
                    weight = validate_float_input(input('Weight (kg): '))
                    if weight is not None:
                        new_product = PhysicalProduct(product_id, product_name, product_price, product_stock, weight)
                        inventory.add_product(new_product)
                        print("Physical product added successfully.")
                elif p_type == '2':
                    download_size = validate_float_input(input('Download Size (MB): '))
                    if download_size is not None:
                        new_product = DigitalProduct(product_id, product_name, product_price, product_stock, download_size)
                        inventory.add_product(new_product)
                        print("Digital product added successfully.")
        case '3':
            product_id = input('Product ID: ')
            product_to_update = inventory.search_product(product_id)
            if product_to_update:
                print(f'Current Stock: {product_to_update.get_stock()}\n')
                new_stock = validate_int_input(input('New Stock Quantity: '))
                if new_stock is not None:
                    product_to_update.update_stock(new_stock)
                    print('\nStock updated successfully!')
        case '4':
            product_id = input('Product ID: ')
            inventory.search_product(product_id)
        case '5':
            save_inventory(file, inventory, option)
        case '6':
            save_inventory(file, inventory, option)
            print('\nThank you for using Inventory Management System.\nProgram terminated.')
            break
        case _:
            print('Invalid option!')