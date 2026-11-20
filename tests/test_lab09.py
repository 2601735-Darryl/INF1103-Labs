import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from discount import BulkDiscount, NoDiscount, PercentageDiscount, StudentDiscount
from inventory import Inventory
from inventory_manager_refactored import get_positive_float, load_products
from order import Order, OrderLine
from product import DigitalProduct, PhysicalProduct
from product_factory import ProductFactory
from supplier import Supplier


class TestLab09DesignPatternsAndErrorHandling(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Test Inc.", "supplier1@test.com")
        self.item_a = ProductFactory.create("physical", "P001", "Desk Lamp", 125.0, 10, self.supplier, weight=1.5)

    # --- Strategy Pattern ---

    def test_order_default_no_discount(self) -> None:
        order = Order("O001")
        order.add_order_line(self.item_a, 2)  # 250.0
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertEqual(order.calculate_total(), 250.0)

    def test_order_bulk_and_percentage_discount_switching(self) -> None:
        order = Order("O002", BulkDiscount(200, 20))
        order.add_order_line(self.item_a, 2)  # 250.0
        self.assertEqual(order.calculate_total(), 230.0)

        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)

    def test_order_student_discount_extension(self) -> None:
        order = Order("O003", StudentDiscount())
        order.add_order_line(self.item_a, 2)  # 250.0 -> 5% off = 237.5
        self.assertEqual(order.calculate_total(), 237.5)

    # --- Factory Pattern ---

    def test_product_factory_creates_subclasses(self) -> None:
        phys = ProductFactory.create("physical", "P010", "Chair", 50.0, 5, self.supplier)
        digi = ProductFactory.create("digital", "D010", "IDE", 99.0, 20, self.supplier)
        self.assertIsInstance(phys, PhysicalProduct)
        self.assertIsInstance(digi, DigitalProduct)

    def test_product_factory_unknown_type_raises_value_error(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "S001", "Installation", 30.0, 5, self.supplier)
        self.assertIn("Unknown product type: service", str(ctx.exception))

    # --- Validation ---

    def test_product_validation_rejects_invalid_price_and_stock(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P011", "Bad Price", 0.0, 5, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P012", "Negative Price", -10.0, 5, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D011", "Negative Stock", 10.0, -1, self.supplier)
        with self.assertRaises(ValueError):
            self.item_a.update_stock(-3)

    def test_order_line_rejects_non_positive_quantity(self) -> None:
        with self.assertRaises(ValueError):
            OrderLine(self.item_a, 0)
        with self.assertRaises(ValueError):
            OrderLine(self.item_a, -2)

    # --- Exception Handling ---

    @patch("builtins.input", side_effect=["abc", "-5", "12.50"])
    def test_get_positive_float_reprompts_until_valid(self, _mock_input) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = get_positive_float("Enter price: ")
        output = buf.getvalue()
        self.assertEqual(result, 12.5)
        self.assertIn("Please enter a valid number, e.g. 12.50", output)
        self.assertIn("Please enter a number greater than zero.", output)

    def test_load_products_missing_file(self) -> None:
        inv = Inventory()
        buf = io.StringIO()
        with redirect_stdout(buf):
            load_products("non_existent_products.csv", inv, self.supplier)
        output = buf.getvalue()
        self.assertIn("Products file not found: non_existent_products.csv", output)
        self.assertIn("Load attempt finished.", output)
        self.assertEqual(len(inv.get_all_products()), 0)

    def test_load_products_skips_bad_rows_and_loads_valid(self) -> None:
        csv_content = (
            "product_type, product_id,name, price, stock_quantity\n"
            "physical, P001, Desk Lamp, 25.00,10\n"
            "digital, D001, Photo Editor, 49.90,100\n"
            "service, S001, Installation, 30.00,5\n"
            "physical, P002, Office Chair, abc, 3\n"
            "physical, P003, Monitor Stand, 39.50,7\n"
        )
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", encoding="utf-8") as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            inv = Inventory()
            buf = io.StringIO()
            with redirect_stdout(buf):
                load_products(tmp_path, inv, self.supplier)
            output = buf.getvalue()
            self.assertEqual(len(inv.get_all_products()), 3)
            self.assertIn("3 products loaded.", output)
            self.assertIn("Load attempt finished.", output)
        finally:
            os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()