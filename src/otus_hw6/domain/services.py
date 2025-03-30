from typing import List

from .models import Product, Order
from .unit_of_work import UnitOfWork


class WarehouseService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def create_product(
        self, name: str, quantity: int, price: float
    ) -> Product:
        with self.uow:
            product = Product(
                id=None, name=name, quantity=quantity, price=price
            )
            self.uow.products.add(product)
            self.uow.commit()
        return product

    def create_order(self, products: List[Product]) -> Order:
        with self.uow:
            order = Order(id=None, products=products)
            self.uow.orders.add(order)
            self.uow.commit()
        return order
