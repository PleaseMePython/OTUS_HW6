from abc import ABC, abstractmethod
from typing import List
from .models import Product, Order


class ProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product):
        raise NotImplementedError

    @abstractmethod
    def get(self, product_id: int) -> Product:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Product]:
        raise NotImplementedError


class OrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order):
        raise NotImplementedError

    @abstractmethod
    def get(self, order_id: int) -> Order:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Order]:
        raise NotImplementedError
