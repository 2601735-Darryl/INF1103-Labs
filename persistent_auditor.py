from pathlib import Path

def get_valid_input(var_type):
    if var_type == '1':
        product = input("Enter Product Name: (type 'q' to quit): ")
        if product.isdigit():
            print("Error! Please enter a string value!")
        else:
            return product
    elif var_type == '2':
        stock = input("Enter Quantity (type 'q' to quit): ")
        if stock == 'q' or stock.isdigit():
            return stock
        else:
            print("Error! Please enter a positive integer!")
            return

def process_delivery(current_value, new_value):
    current_value += new_value
    return current_value

def calculate_tax(amount):
    amount *= (1/10)
    print(f'Total tax amount: ${amount}')
    return amount

def generate_report(total_units, failed_attempts):
    print(f"Total units processed: {total_units}\nNumber of Failed/Rejected entries: {failed_attempts}")
    return

def load_inventory(file_path):
    if file_path.is_file():
        with open(file_path,'r',encoding="utf-8") as file:
            content = file.read()
            return content
    else:
        with open(file_path,'x',encoding="utf-8") as file:
            return []

def append_inventory(inv_list,new_order):
    inv_list = inv_list.append(new_order)
    print(f'New Order Added: {new_order}')

inventory = load_inventory(Path('INF-1103-Labs/inventory.txt'))
failed_entries = 0
delivery_fee = 0

while True:
    if inventory == []:
        order_id = 1001
    else:
        print('Current Orders: \n\n')
        for i in inventory:
            print(*i,sep=', ')
        order_id = int(inventory[-1][0]) + 1

    product  = get_valid_input('1')
    if product != None:
        if product == 'q':
            generate_report(inventory,failed_entries)
            break
        else:
            quantity = get_valid_input('2')
            if quantity != None:
                if quantity == 'q':
                    generate_report(inventory,failed_entries)
                    # calculate_tax(inventory*5) # delivery for each unit is $5
                    break
                elif quantity.isdigit():
                    append_inventory(inventory,[order_id,product,quantity])
                    print(f'Current inventory: {inventory}')
            else:
                failed_entries += 1
    else:
        failed_entries += 1