from dataclasses import dataclass, field
from typing import List


@dataclass
class Product:
    id: int
    name: str
    quantity: int
    price: float

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (
            isinstance(other, Product)  # ORM должен наследовать сущности
            and self.id == other.id
            and self.name == other.name
            and self.quantity == other.quantity
            and self.price == other.price
        )


@dataclass
class Order:
    id: int
    products: List[Product] = field(default_factory=list)

    def add_product(self, product: Product):
        self.products.append(product)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (
            isinstance(other, Order)  # ORM должен наследовать сущности
            and self.id == other.id
            and len(self.products) == len(other.products)
            and (
                self_prod == other_prod
                for self_prod, other_prod in zip(
                    sorted(self.products, key=lambda prod: prod.id),
                    sorted(other.products, key=lambda prod: prod.id),
                )
            )
        )
