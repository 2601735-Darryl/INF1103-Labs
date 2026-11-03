class Inventory():
    def __init__(self):
        self._products = []

    def add_product(self,product):
        self._products.append(product)

    def search_product(self,product_id):
        found = False
        for product in self._products:
            if product.get_product_id() == product_id:
                print('Product Found!\n------------------------------------------------')
                product.display_information()
                found = True
                return product
        if found == False:
            print('Product cannot be found!')
            return None

    def display_all(self):
        print('All Products\n------------------------------------------------')
        for product in self._products:
            product.display_information()

    def get_all_products(self):
        return self._products