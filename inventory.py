class Inventory():
    def __init__(self):
        self.__products = []

    def add_product(self,product):
        self.__products.append(product)

    def search_product(self,product_id):
        found = False
        for product in self.__products:
            if product.get_product_id() == product_id:
                print('Product Found!\n------------------------------------------------')
                product.display_information()
                found = True
        if found == False:
            print('Product cannot be found!')

    def display_all(self):
        print('All Products\n------------------------------------------------')
        for product in self.__products:
            product.display_information()
        