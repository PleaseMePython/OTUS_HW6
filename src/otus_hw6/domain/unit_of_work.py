from typing import Self

from abc import ABC, abstractmethod

from .repositories import ProductRepository, OrderRepository


class UnitOfWork(ABC):
    orders: OrderRepository
    products: ProductRepository

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
