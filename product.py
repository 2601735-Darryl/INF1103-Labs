class Product:
    def __init__(self,product_id,name,price,stock):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = stock

    def update_stock(self,quantity):
        self._stock = quantity

    def display_information(self):
        print(f'''Product Information
------------------------------------------------     
Product ID: {self._product_id}
Name: {self._name}
Price: {self._price}
Stock: {self._stock}
------------------------------------------------
''')
    def get_product_id(self):
        return self._product_id