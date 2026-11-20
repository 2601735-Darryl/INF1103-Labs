from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        if not (0 <= percentage <= 100):
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)

class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, discount_amount: float) -> None:
        if threshold <= 0 or discount_amount < 0:
            raise ValueError("Threshold must be positive and discount amount cannot be negative.")
        self.threshold: float = threshold
        self.discount_amount: float = discount_amount

    def apply(self, total: float) -> float:
        return total - self.discount_amount if total >= self.threshold else total
