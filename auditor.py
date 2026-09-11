inventory = 0
while True:
    stock = input("Enter stock quantity (type 'q' to quit): ")
    if stock == 'q':
        break
    elif inventory > 500:
        print("Inventory exceeding 500 units")
    elif stock.isdigit():
            inventory += int(stock)
            if inventory > 500:
                print("Inventory exceeding 500 units!")   
                break
            print(inventory)
    else:
        print("Error! Please enter a positive integer!")
