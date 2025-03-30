import pytest


from .sqlite_queries import (
    sqlite_cleanup_db,
    select_all_products,
    select_all_orders,
)
from src.otus_hw6.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


class TestUnitOfWork:
    @staticmethod
    def clean_db(sqlite_session_factory):
        cleanup_session = sqlite_session_factory()
        sqlite_cleanup_db(session=cleanup_session)
        cleanup_session.commit()
        cleanup_session.close()

    def test_can_save_orders(self, sqlite_session_factory, orders_expected):
        self.clean_db(sqlite_session_factory)
        orders = orders_expected[0:1]
        uow = SqlAlchemyUnitOfWork(sqlite_session_factory)
        with uow:
            uow.orders.add(orders[0])
            uow.commit()

        new_session = sqlite_session_factory()
        rows = select_all_orders(session=new_session)
        assert rows == orders

    def test_can_save_products(
        self, sqlite_session_factory, products_expected
    ):
        self.clean_db(sqlite_session_factory)
        products = products_expected[0:1]
        uow = SqlAlchemyUnitOfWork(sqlite_session_factory)
        with uow:
            uow.products.add(products[0])
            uow.commit()

        new_session = sqlite_session_factory()
        rows = select_all_products(session=new_session)
        assert rows == products

    def test_rolls_back_uncommitted_work_by_default(
        self, sqlite_session_factory, orders_expected
    ):
        self.clean_db(sqlite_session_factory)

        uow = SqlAlchemyUnitOfWork(sqlite_session_factory)
        with uow:
            uow.orders.add(orders_expected[0])

        new_session = sqlite_session_factory()
        rows = select_all_orders(session=new_session)
        assert rows == []

    def test_rolls_back_on_error(
        self, sqlite_session_factory, orders_expected
    ):
        class MyException(Exception):
            pass

        self.clean_db(sqlite_session_factory)

        uow = SqlAlchemyUnitOfWork(sqlite_session_factory)
        with pytest.raises(MyException):
            with uow:
                uow.orders.add(orders_expected[0])
                raise MyException()

        new_session = sqlite_session_factory()
        rows = select_all_orders(session=new_session)
        assert rows == []
