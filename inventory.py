from product import Product

class Inventory:
    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
        
    def remove_product(self, product_id: str) -> None:
        product = self.find_product(product_id)
        if product:
            self.products.remove(product)
            print(f"Product {product_id} removed from inventory.")

    def search_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product:
            print('Product Found!\n------------------------------------------------')
            product.display_information()
            return product
        print('Product cannot be found!')
        return None

    def display_all(self) -> None:
        print('All Products\n------------------------------------------------')
        for product in self.products:
            product.display_information()

    def get_all_products(self) -> list[Product]:
        return self.products