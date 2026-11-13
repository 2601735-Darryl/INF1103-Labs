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
        self.stock = quantity

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
        return self.product_id

    def get_stock(self):
        return self.stock

    def to_dict(self):
        return {
            'ID': self.product_id,
            'Name': self.name,
            'Price': f"${self.price}" if isinstance(self.price, float) else self.price,
            'Stock': self.stock
        }

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.weight: float = weight

    def display_information(self):
        super().display_information()
        print(f'Weight: {self.weight}kg')
        print(f'Fulfilment: {self.get_fulfilment_info()}')
        print(f'Shipping Cost: ${self.calculate_shipping_cost():.2f}')
        print('------------------------------------------------\n')

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        return self.weight * 2.0
    
    def to_dict(self):
        data = super().to_dict()
        data['Type'] = 'Physical'
        data['Weight'] = self.weight
        return data

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.download_size: float = download_size

    def display_information(self):
        super().display_information()
        print(f'Download Size: {self.download_size}MB')
        print(f'Fulfilment: {self.get_fulfilment_info()}')
        print('------------------------------------------------\n')

    def get_fulfilment_info(self):
        return "This product is delivered digitally via a download link."

    def to_dict(self):
        data = super().to_dict()
        data['Type'] = 'Digital'
        data['DownloadSize'] = self.download_size
        return data