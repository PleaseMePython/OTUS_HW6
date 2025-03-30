from typing import List

from .sqlite_queries import (
    insert_products,
    insert_orders,
    select_all_orders,
    select_all_products,
)

from src.otus_hw6.domain.models import Product
from src.otus_hw6.infrastructure.orm import OrderORM, ProductORM


class TestORM:
    def test_products_can_be_read(self, sqlite_session, products_expected):
        insert_products(session=sqlite_session, products=products_expected)

        sqlite_session.commit()

        rows = sqlite_session.query(ProductORM).order_by(ProductORM.id).all()

        assert len(rows) == len(products_expected)
        for row, exp in zip(rows, products_expected):
            assert row == exp

    def test_products_can_be_saved(self, sqlite_session, products_expected):
        for exp in products_expected:
            sqlite_session.add(
                ProductORM(
                    id=None,
                    name=exp.name,
                    quantity=exp.quantity,
                    price=exp.price,
                )
            )

        sqlite_session.commit()

        rows: List[Product] = select_all_products(session=sqlite_session)

        assert len(rows) == len(products_expected)
        for row, exp in zip(rows, products_expected):
            assert row == exp

    def test_orders_can_be_read(self, sqlite_session, orders_expected):
        insert_orders(session=sqlite_session, orders=orders_expected)

        sqlite_session.commit()

        rows = sqlite_session.query(OrderORM).order_by(OrderORM.id).all()

        assert len(rows) == len(orders_expected)
        for row, exp in zip(rows, orders_expected):
            assert row == exp

    def test_orders_can_be_saved(
        self, sqlite_session, orders_expected, products_expected
    ):
        for exp in orders_expected:
            sqlite_session.add(
                OrderORM(
                    id=None,
                    products=[
                        ProductORM(
                            id=p.id,
                            name=p.name,
                            quantity=p.quantity,
                            price=p.price,
                        )
                        for p in exp.products
                    ],
                )
            )

        sqlite_session.commit()

        orders_db = select_all_orders(session=sqlite_session)

        assert len(orders_db) == len(orders_expected)
        for row, exp in zip(orders_db, orders_expected):
            assert row == exp
