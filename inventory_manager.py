from pathlib import Path
import os
import json

def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False
    
def validate_str_input(user_input):
    if user_input.isdigit() or user_input.strip() == '':
        print("Error! Please enter a string value!")
        return
    else:
         return user_input

def validate_int_input(user_input):
    if user_input.isdigit() and int(user_input) > 0:
        return user_input
    else:
        print("Error! Please enter a positive integer!")
        return

def validate_float_input(user_input):
    if is_float(user_input) and float(user_input) > 0:
        return user_input
    else:
        print("Error! Please enter a positive float value!")
        return
    
def load_inventory(file_path):
    if os.path.exists(file_path):
        if os.path.getsize(file_path) != 0:
            try:
                with open(file_path,'r',encoding="utf-8") as file:
                    content = json.load(file)
                    return content
            except json.JSONDecodeError:
                return []
    else:
        with open(file_path,'x',encoding="utf-8") as file:
            return []

def append_inventory(inv_list,new_order):
    inv_list = inv_list.append(new_order)
    print(f'New Order Added:\n{", ".join(new_order)}')

def save_inventory(file_path,inv_list,menu_option):
    with open(file_path,'w',encoding="utf-8") as file:
        json.dump(inv_list, file, indent=4)
    if menu_option == '5':
        print(f'\nSaving inventory...\nInventory saved to {file_path}')
    else:
        print('\nSaving inventory before exit...Inventory saved successfully.')


def add_product(p_list,p_id,p_name,p_price,p_stock):
    p_list = p_list.append({
        'ID' : p_id,
        'Name' : p_name,
        'Price' : '$' + p_price,
        'Stock' : p_stock
    })
    print('\nProduct added successfully!')

def display_all(p_list):
    print('\n------------------------------------------------')
    for i in p_list:
        print(f"ID: {i['ID']} | Name: {i['Name']} | Price: {i['Price']} | Stock: {i['Stock']}")
    print('------------------------------------------------')

def update_stock(p_list,p_id):
    found = 0
    for i in p_list:
        if i['ID'] == p_id:
            print(f'\nProduct Found:\nName: {i["Name"]}\nCurrent Stock: {i["Stock"]}\n')
            new_p_stock = validate_int_input(input('New Stock Quantity: '))
            i["Stock"] = new_p_stock
            print('\nStock updated successfully!')
            found = 1
            return i
    if found == 0:
        print('Product not found.')

def search_product(p_list,p_id):
    found = 0
    for i in p_list:
        if i['ID'] == p_id:
            print(f'''
Product Found
------------------------------------------------
ID : {i["ID"]}
Name: {i["Name"]}
Price: {i["Price"]}
Stock: {i["Stock"]}
------------------------------------------------\n
''')
            found = 1
            return i
    if found == 0:
        print('Product not found.')


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
        