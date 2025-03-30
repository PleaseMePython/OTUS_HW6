from typing import List

from .sqlite_queries import (
    select_all_products,
    select_all_orders,
    insert_orders,
    insert_products,
)

from src.otus_hw6.domain.models import Product
from src.otus_hw6.infrastructure.repositories import (
    SqlAlchemyOrderRepository,
    SqlAlchemyProductRepository,
)


class TestProductRepository:
    def test_repository_can_save_product(
        self, sqlite_session, products_expected
    ):
        repo = SqlAlchemyProductRepository(session=sqlite_session)
        products = products_expected[0:1]
        repo.add(product=products[0])
        sqlite_session.commit()

        rows: List[Product] = select_all_products(session=sqlite_session)

        assert len(rows) == len(products)
        for row, exp in zip(rows, products):
            assert row == exp

    def test_repository_can_read_product(
        self, sqlite_session, products_expected
    ):
        products = products_expected[0:1]
        insert_products(session=sqlite_session, products=products)
        sqlite_session.commit()

        repo = SqlAlchemyProductRepository(session=sqlite_session)
        rows = [repo.get(product_id=products[0].id)]

        assert len(rows) == len(products)
        for row, exp in zip(rows, products):
            assert row == exp

    def test_repository_list(self, sqlite_session, products_expected):
        insert_products(session=sqlite_session, products=products_expected)
        sqlite_session.commit()

        repo = SqlAlchemyProductRepository(session=sqlite_session)
        rows = repo.list()

        assert len(rows) == len(products_expected)
        for row, exp in zip(rows, products_expected):
            assert row == exp


class TestOrderRepository:
    def test_repository_can_save_order(self, sqlite_session, orders_expected):
        repo = SqlAlchemyOrderRepository(session=sqlite_session)
        orders = orders_expected[0:1]
        repo.add(order=orders[0])
        sqlite_session.commit()

        rows = select_all_orders(session=sqlite_session)

        assert len(rows) == len(orders)
        for row, exp in zip(rows, orders):
            assert row == exp

    def test_repository_can_read_order(self, sqlite_session, orders_expected):
        orders = orders_expected[0:1]
        insert_orders(session=sqlite_session, orders=orders)
        sqlite_session.commit()

        repo = SqlAlchemyOrderRepository(session=sqlite_session)
        rows = [repo.get(order_id=orders[0].id)]

        assert len(rows) == len(orders)
        for row, exp in zip(rows, orders):
            assert row == exp

    def test_repository_list(self, sqlite_session, orders_expected):
        insert_orders(session=sqlite_session, orders=orders_expected)
        sqlite_session.commit()

        repo = SqlAlchemyOrderRepository(session=sqlite_session)
        rows = repo.list()

        assert len(rows) == len(orders_expected)
        for row, exp in zip(rows, orders_expected):
            assert row == exp
