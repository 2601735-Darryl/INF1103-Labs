from abc import ABC, abstractmethod

class Product:
    def __init__(self,product_id,name,price,stock):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = stock

    def update_stock(self,quantity):
        self._stock = quantity

    @abstractmethod
    def get_fulfilment_info(self):
        pass

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

    def get_stock(self):
        return self._stock

    def to_dict(self):
        return {
            'ID': self._product_id,
            'Name': self._name,
            'Price': f"${self._price}" if isinstance(self._price, float) else self._price,
            'Stock': self._stock
        }

class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self._weight = weight

    def display_information(self):
        super().display_information()
        print(f'Weight: {self._weight}kg')
        print('------------------------------------------------\n')

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def to_dict(self):
        data = super().to_dict()
        data['Type'] = 'physical'
        data['Weight'] = self._weight
        return data

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self._download_size = download_size

    def display_information(self):
        super().display_information()
        print(f'Download Size: {self._download_size}MB')
        print('------------------------------------------------\n')

    def get_fulfilment_info(self):
        return "This product is delivered digitally via a download link."

    def to_dict(self):
        data = super().to_dict()
        data['Type'] = 'digital'
        data['DownloadSize'] = self._download_size
        return data