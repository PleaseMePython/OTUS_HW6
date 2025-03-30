from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from ..domain.models import Order, Product
from ..domain.repositories import ProductRepository, OrderRepository
from .orm import ProductORM, OrderORM


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    def add(self, product: Product):
        product_orm = ProductORM(
            id=None,
            name=product.name,
            quantity=product.quantity,
            price=product.price,
        )
        self.session.add(product_orm)

    def get(self, product_id: int) -> Product:
        product_orm: ProductORM = self.session.scalars(
            select(ProductORM).filter_by(id=product_id)
        ).one()
        return Product(
            id=product_orm.id,
            name=product_orm.name,
            quantity=product_orm.quantity,
            price=product_orm.price,
        )

    def list(self) -> List[Product]:
        products_orm = self.session.scalars(select(ProductORM)).all()
        return [
            Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
            for p in products_orm
        ]


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, order: Order):
        order_orm = OrderORM(
            id=None,
            products=[
                ProductORM(
                    id=p.id, name=p.name, quantity=p.quantity, price=p.price
                )
                for p in order.products
            ],
        )
        self.session.add(order_orm)

    def get(self, order_id: int) -> Order:
        order_orm: OrderORM = self.session.scalars(
            select(OrderORM).filter_by(id=order_id)
        ).one()
        products = [
            Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
            for p in order_orm.products
        ]
        return Order(id=order_orm.id, products=products)

    def list(self) -> List[Order]:
        orders_orm = self.session.scalars(select(OrderORM)).all()
        orders = []
        for order_orm in orders_orm:
            products = [
                Product(
                    id=p.id, name=p.name, quantity=p.quantity, price=p.price
                )
                for p in order_orm.products
            ]
            orders.append(Order(id=order_orm.id, products=products))
        return orders
