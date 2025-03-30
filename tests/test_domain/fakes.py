from typing import List

from src.otus_hw6.domain.models import Product, Order
from src.otus_hw6.domain.repositories import ProductRepository, OrderRepository
from src.otus_hw6.domain.unit_of_work import UnitOfWork


class FakeProductRepository(ProductRepository):
    def __init__(self, products: List[Product]):
        self._products = set(products)
        self._max_id = 0

    def add(self, product: Product):
        if product.id is None:
            self._max_id += 1
        elif product.id > self._max_id:
            self._max_id = product.id

        self._products.add(
            Product(
                id=self._max_id if product.id is None else product.id,
                name=product.name,
                quantity=product.quantity,
                price=product.price,
            )
        )

    def get(self, product_id: int):
        return next(b for b in self._products if b.id == product_id)

    def list(self):
        return list(self._products)


class FakeOrderRepository(OrderRepository):
    def __init__(self, orders: List[Order]):
        self._orders = set(orders)
        self._max_id = 0
        self.products = FakeProductRepository([])

    def add(self, order: Order):
        self._max_id += 1
        self._orders.add(Order(id=self._max_id, products=order.products))
        for p in order.products:
            self.products.add(p)

    def get(self, order_id: int):
        return next(b for b in self._orders if b.id == order_id)

    def list(self):
        return list(self._orders)


class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        fake_rep = FakeOrderRepository([])
        self.orders = fake_rep
        self.products = fake_rep.products
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
