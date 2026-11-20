import csv
import json
import os
from pathlib import Path

from discount import BulkDiscount, PercentageDiscount, StudentDiscount
from inventory import Inventory
from order import Order
from product import Product
from product_factory import ProductFactory
from supplier import Supplier

DEFAULT_SUPPLIER = Supplier("S001", "Test Inc.", "supplier1@test.com")

def get_non_empty_str(prompt: str) -> str:
    while True:
        user_input = input(prompt).strip()
        if not user_input or user_input.isdigit():
            print("Please enter a valid non-numeric string.")
            continue
        return user_input


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number that is zero or greater.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 10")

def load_inventory(file_path: Path) -> Inventory:
    inventory_obj = Inventory()
    if os.path.exists(file_path):
        if os.path.getsize(file_path) != 0:
            try:
                with open(file_path, 'r', encoding="utf-8") as file:
                    content = json.load(file)
                    for item in content:
                        try:
                            raw_price = (
                                item['Price'].replace('$', '')
                                if isinstance(item['Price'], str)
                                else item['Price']
                            )
                            product_type = item.get('Type', 'Physical')
                            weight = float(item.get('Weight', 1.0))
                            download_size = float(item.get('DownloadSize', 100.0))

                            product = ProductFactory.create(
                                product_type=product_type,
                                product_id=item['ID'],
                                name=item['Name'],
                                price=float(raw_price),
                                stock_quantity=int(item['Stock']),
                                supplier=DEFAULT_SUPPLIER,
                                weight=weight,
                                download_size=download_size,
                            )
                            inventory_obj.add_product(product)
                        except (KeyError, ValueError) as err:
                            print(f"Skipping invalid JSON item {item}: {err}")
            except json.JSONDecodeError:
                print(f"Warning: {file_path} contains invalid JSON.")
    else:
        try:
            with open(file_path, 'x', encoding="utf-8"):
                pass
        except OSError as err:
            print(f"Unable to create {file_path}: {err}")
    return inventory_obj


def load_products(path: str, inventory_obj: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row
            for row in reader:
                if not row:
                    continue
                try:
                    if len(row) < 5:
                        raise ValueError("Incomplete row data")
                    product_type = row[0].strip()
                    product_id = row[1].strip()
                    name = row[2].strip()
                    price = float(row[3].strip())
                    stock_quantity = int(row[4].strip())

                    product = ProductFactory.create(
                        product_type, product_id, name, price, stock_quantity, supplier
                    )
                    inventory_obj.add_product(product)
                    loaded += 1
                except ValueError as err:
                    print(f"Skipping invalid row {row}: {err}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def save_inventory(file_path: Path, inventory_obj: Inventory, menu_option: str) -> None:
    inv_list = [product.to_dict() for product in inventory_obj.get_all_products()]
    try:
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(inv_list, file, indent=4)
        if menu_option == '5':
            print(f'\nSaving inventory...\nInventory saved to {file_path}')
        else:
            print('\nSaving inventory before exit...Inventory saved successfully.')
    except OSError as err:
        print(f"Error saving inventory: {err}")

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())

def test_lsp() -> None:
    print("\n---Testing LSP (via ProductFactory)---")
    test_supplier = Supplier("S067", "Test Supplier", "test@gmail.com")
    physical_test = ProductFactory.create("physical", "P067", "Test Book", 15.0, 10, test_supplier, weight=0.5)
    digital_test = ProductFactory.create("digital", "D067", "Test E-Book", 2.0, 10, test_supplier, download_size=5.0)

    print("Testing Physical Product LSP:")
    show_product_details(physical_test)

    print("Testing Digital Product LSP:")
    show_product_details(digital_test)

def test_polymorphism(inventory_obj: Inventory) -> None:
    print("\n---Testing Polymorphism---")
    if not inventory_obj.products:
        print("Inventory is empty. Add products to test polymorphism.")
        return

    for product in inventory_obj.products:
        product.display_information()
        print(f"Fulfilment Details: {product.get_fulfilment_info()}\n")

def demo_order_discounts(inventory_obj: Inventory) -> None:
    print("\n---Strategy Pattern on Order---")
    products = inventory_obj.get_all_products()
    if not products:
        print("No products available to create a sample order.")
        return

    sample_product = ProductFactory.create("physical", "P999", "Sample Item", 125.0, 10, DEFAULT_SUPPLIER, weight=1.0)
    order = Order("ORD-001", BulkDiscount(200, 20))
    order.add_order_line(sample_product, 2)  # Subtotal = 250.0
    print(f"BulkDiscount(200, 20) Total: ${order.calculate_total():.2f}")

    order.set_discount(PercentageDiscount(10))
    print(f"PercentageDiscount(10) Total: ${order.calculate_total():.2f}")

    order.set_discount(StudentDiscount())
    print(f"StudentDiscount(5%) Total: ${order.calculate_total():.2f}")


# --- Main CLI Loop ---

if __name__ == "__main__":
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

    test_lsp()
    test_polymorphism(inventory)

    while True:
        print('''
----------- MENU -----------
1. Display All Products
2. Add Product
3. Update Stock
4. Search Product
5. Save Inventory
6. Load Products from CSV (products.csv)
7. Demo Order Discounts
8. Exit
----------------------------
''')
        option = input("\nEnter option: ").strip()
        match option:
            case '1':
                inventory.display_all()
            case '2':
                print('Add New Product')
                p_type_choice = input('Enter Product Type (1 for Physical, 2 for Digital): ').strip()
                if p_type_choice not in ['1', '2']:
                    print("Invalid product type selected.")
                    continue

                product_id = get_non_empty_str('Product ID: ')
                product_name = get_non_empty_str('Product Name: ')
                product_price = get_positive_float('Price: ')
                product_stock = get_non_negative_int('Stock Quantity: ')

                try:
                    if p_type_choice == '1':
                        weight = get_positive_float('Weight (kg): ')
                        new_product = ProductFactory.create(
                            "physical", product_id, product_name, product_price, product_stock, DEFAULT_SUPPLIER, weight=weight
                        )
                        inventory.add_product(new_product)
                        print("Physical product added successfully.")
                    else:
                        download_size = get_positive_float('Download Size (MB): ')
                        new_product = ProductFactory.create(
                            "digital", product_id, product_name, product_price, product_stock, DEFAULT_SUPPLIER, download_size=download_size
                        )
                        inventory.add_product(new_product)
                        print("Digital product added successfully.")
                except ValueError as err:
                    print(f"Failed to add product: {err}")
            case '3':
                product_id = input('Product ID: ').strip()
                product_to_update = inventory.search_product(product_id)
                if product_to_update:
                    print(f'Current Stock: {product_to_update.get_stock()}\n')
                    new_stock = get_non_negative_int('New Stock Quantity: ')
                    try:
                        product_to_update.update_stock(new_stock)
                        print('\nStock updated successfully!')
                    except ValueError as err:
                        print(f"Error updating stock: {err}")
            case '4':
                product_id = input('Product ID: ').strip()
                inventory.search_product(product_id)
            case '5':
                save_inventory(file, inventory, option)
            case '6':
                load_products("products.csv", inventory, DEFAULT_SUPPLIER)
            case '7':
                demo_order_discounts(inventory)
            case '8':
                save_inventory(file, inventory, option)
                print('\nThank you for using Inventory Management System.\nProgram terminated.')
                break
            case _:
                print('Invalid option!')