from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..domain.unit_of_work import UnitOfWork

from .repositories import (
    SqlAlchemyOrderRepository,
    SqlAlchemyProductRepository,
)

from .database import DATABASE_URL

DEFAULT_ENGINE = create_engine(DATABASE_URL)

DEFAULT_SESSION_FACTORY = sessionmaker(bind=DEFAULT_ENGINE)


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.products = SqlAlchemyProductRepository(self.session)
        self.orders = SqlAlchemyOrderRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
