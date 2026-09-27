from pathlib import Path
def get_valid_input():
    stock = input("Enter stock quantity (type 'q' to quit): ")
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
            pass

inventory = 0
failed_entries = 0
delivery_fee = 0

load_inventory(Path('INF-1103-Labs/inventory.txt'))

while True:
    user_input = get_valid_input()
    if user_input != None:
        if user_input == 'q':
            generate_report(inventory,failed_entries)
            calculate_tax(inventory*5) # delivery for each unit is $5
            break
        elif user_input.isdigit():
            inventory = process_delivery(inventory, int(user_input))
            print(f'Current inventory: {inventory}')
    else:
        failed_entries += 1