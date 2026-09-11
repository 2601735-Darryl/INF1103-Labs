inventory = 0
failed_entries = 0
while True:
    stock = input("Enter stock quantity (type 'q' to quit): ")
    if stock == 'q':
        print(f"Total units processed: {inventory}\nNumber of Failed/Rejected entries: {failed_entries}")
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
        failed_entries += 1
        print("Error! Please enter a positive integer!")
