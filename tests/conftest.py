import pytest


from typing import List

from .test_infrastructure.sqlite_queries import sqlite_cleanup_db

from src.otus_hw6.domain.models import Product, Order

from src.otus_hw6.infrastructure.orm import Base
from src.otus_hw6.infrastructure.unit_of_work import (
    DEFAULT_ENGINE,
    DEFAULT_SESSION_FACTORY,
)


@pytest.fixture
def sqlite_db():
    engine = DEFAULT_ENGINE
    Base.metadata.create_all(DEFAULT_ENGINE)
    return engine


@pytest.fixture
def sqlite_session_factory(sqlite_db):
    return DEFAULT_SESSION_FACTORY


@pytest.fixture
def sqlite_session(sqlite_session_factory):
    # clear_mappers()
    # configure_mappers()
    session = sqlite_session_factory()
    sqlite_cleanup_db(session)
    session.commit()
    yield session
    sqlite_cleanup_db(session)
    session.commit()
    # clear_mappers()


@pytest.fixture
def products_expected() -> List[Product]:
    return [
        Product(id=1, name="product1", quantity=10, price=12.1),
        Product(id=2, name="product2", quantity=20, price=24.3),
        Product(id=3, name="product3", quantity=40, price=48.7),
        Product(id=4, name="product4", quantity=60, price=85.4),
    ]


@pytest.fixture
def orders_expected(products_expected) -> List[Order]:
    return [
        Order(id=1, products=products_expected[0:2]),
        Order(id=2, products=products_expected[2:4]),
    ]
