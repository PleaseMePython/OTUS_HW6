from typing import List
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase, registry, MappedAsDataclass

from ..domain.models import Order, Product

mapper_registry = registry()


# declarative base class
class Base(MappedAsDataclass, DeclarativeBase):
    pass


order_product_associations = Table(
    "order_product_associations",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id")),
    Column("product_id", ForeignKey("products.id")),
)


class OrderORM(Order, Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    products: Mapped[List["ProductORM"]] = relationship(
        secondary=order_product_associations
    )


class ProductORM(Product, Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column()
