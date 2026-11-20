from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        if price <= 0:
            raise ValueError("Product price must be greater than zero.")
        if stock < 0:
            raise ValueError("Product stock quantity cannot be negative.")

        self.product_id: str = product_id
        self.name: str = name
        self.price: float = price
        self.stock: int = stock
        self.supplier: Supplier = supplier

    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Product stock quantity cannot be negative.")
        self.stock = quantity

    @abstractmethod
    def get_fulfilment_info(self) -> str:
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

    def get_product_id(self) -> str:
        return self.product_id

    def get_stock(self) -> int:
        return self.stock

    def to_dict(self) -> dict:
        return {
            'ID': self.product_id,
            'Name': self.name,
            'Price': f"${self.price}" if isinstance(self.price, float) else self.price,
            'Stock': self.stock
        }


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(
        self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if weight <= 0:
            raise ValueError("Physical product weight must be greater than zero.")
        self.weight: float = weight

    def display_information(self) -> None:
        super().display_information()
        print(f'Weight: {self.weight}kg')
        print(f'Fulfilment: {self.get_fulfilment_info()}')
        print(f'Shipping Cost: ${self.calculate_shipping_cost():.2f}')
        print('------------------------------------------------\n')

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return self.weight * 2.0

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['Type'] = 'Physical'
        data['Weight'] = self.weight
        return data


class DigitalProduct(Product):
    def __init__(
        self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if download_size <= 0:
            raise ValueError("Digital product download size must be greater than zero.")
        self.download_size: float = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f'Download Size: {self.download_size}MB')
        print(f'Fulfilment: {self.get_fulfilment_info()}')
        print('------------------------------------------------\n')

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally via a download link."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['Type'] = 'Digital'
        data['DownloadSize'] = self.download_size
        return data