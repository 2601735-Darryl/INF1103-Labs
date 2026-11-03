import os
import json
from pathlib import Path
from inventory import Inventory
from product import Product

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
                        # Strip the '$' from the JSON file to store as a float inside the object
                        raw_price = item['Price'].replace('$', '') if isinstance(item['Price'], str) else item['Price']
                        product = Product(item['ID'], item['Name'], float(raw_price), item['Stock'])
                        inventory_obj._products.append(product) # Load silently without triggering the "added successfully" print
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
if inventory == []:
    print(f'{file} either not found, is empty or is in an invalid format.')

else:
        print(f'{file} found.\nInventory loaded successfully.\n')

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
while True:
    option = input("\nEnter option: ")
    match option:
        case '1':
            display_all(inventory)
        case '2':
            print('Add New Product')
            product_id = validate_str_input(input('Product ID: '))
            product_name = validate_str_input(input('Product Name: '))
            product_price = validate_float_input(input('Price: '))
            product_stock = validate_int_input(input('Stock Quantity: '))
            add_product(inventory,product_id,product_name,product_price,int(product_stock))
        case '3':
            product_id = input('Product ID: ')
            update_stock(inventory,product_id)
        case '4':
            product_id = input('Product ID: ')
            search_product(inventory,product_id)
        case '5':
            save_inventory(file,inventory,option)
        case '6':
            save_inventory(file,inventory,option)
            print('\nThank you for using Inventory Management System.\nProgram terminated.')
            break
        case _:
            print('Invalid option!')
        