from abc import ABC, abstractmethod
from supplier import Supplier

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        self.product_id: str = product_id
        self.name: str = name
        self.price: float = price
        self.stock: int = stock
        self.supplier: Supplier = supplier

    def update_stock(self,quantity):
        self._stock = quantity

    @abstractmethod
    def get_fulfilment_info(self):
        pass

    def display_information(self) -> None:
        print(f'''Product Information
------------------------------------------------     
Product ID: {self.product_id}
Name: {self.name}
Price: {self.price}
Stock: {self.stock}
Supplier: {self.supplier.name} ({self.supplier.contact_email})
------------------------------------------------''')
        
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

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self._weight = weight

    def display_information(self):
        super().display_information()
        print(f'Weight: {self._weight}kg')
        print(f'Fulfilment: {self.get_fulfilment_info()}')
        print(f'Shipping Cost: ${self.calculate_shipping_cost():.2f}')
        print('------------------------------------------------\n')

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        return self._weight * 2.0
    
    def to_dict(self):
        data = super().to_dict()
        data['Type'] = 'Physical'
        data['Weight'] = self._weight
        return data

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self._download_size = download_size

    def display_information(self):
        super().display_information()
        print(f'Download Size: {self._download_size}MB')
        print(f'Fulfilment: {self.get_fulfilment_info()}')
        print('------------------------------------------------\n')

    def get_fulfilment_info(self):
        return "This product is delivered digitally via a download link."

    def to_dict(self):
        data = super().to_dict()
        data['Type'] = 'Digital'
        data['DownloadSize'] = self._download_size
        return data