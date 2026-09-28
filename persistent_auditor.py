from pathlib import Path

def get_valid_input(var_type):
    if var_type == 'str':
        product = input("Enter Product Name: (type 'q' to quit): ")
        if product.isdigit() or product.strip() == '':
            print("Error! Please enter a string value!")
            return
        else:
            return product
    elif var_type == 'num':
        stock = input("Enter Quantity (type 'q' to quit): ")
        if stock == 'q' or stock.isdigit() and stock == 0:
            return stock
        else:
            print("Error! Please enter a positive integer!")
            return

def load_inventory(file_path):
    if file_path.is_file():
        with open(file_path,'r',encoding="utf-8") as file:
            content = file.read()
            content = [row.split(', ') for row in content.splitlines()]
            return content
    else:
        with open(file_path,'x',encoding="utf-8") as file:
            return []

def append_inventory(inv_list,new_order):
    inv_list = inv_list.append(new_order)
    print(f'New Order Added:\n{", ".join(new_order)}')

def save_inventory(file_path,inv_list):
    with open(file_path,'w',encoding="utf-8") as file:
        for i in inv_list:
            list_str = ', '.join(i)
            file.write(f'{list_str}\n')
    print(f'Order successfully saved to {file_path}')

file = Path('INF-1103-Labs/inventory.txt')
inventory = load_inventory(file)

while True:
    if inventory == []:
        order_id = '1001'
    else:
        print('Current Orders: \n\n')
        for i in inventory:
            print(*i,sep=', ')
        print('\n')
        order_id = str(int(inventory[-1][0]) + 1)

    product  = get_valid_input('str')
    if product != None:
        if product == 'q':
            save_inventory(file,inventory)
            break
        else:
            quantity = get_valid_input('num')
            if quantity != None:
                if quantity == 'q':
                    save_inventory(file,inventory)
                    break
                else:
                    append_inventory(inventory,[order_id,product,quantity])