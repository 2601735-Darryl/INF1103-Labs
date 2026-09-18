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