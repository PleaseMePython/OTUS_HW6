from tests.test_domain.fakes import FakeUnitOfWork
from src.otus_hw6.domain.services import WarehouseService


class TestServices:
    def test_create_product(self, products_expected):
        uow = FakeUnitOfWork()
        services = WarehouseService(uow=uow)
        product = products_expected[0]
        services.create_product(
            name=product.name, quantity=product.quantity, price=product.price
        )
        assert uow.products.get(product_id=product.id) is not None
        assert uow.committed

    def test_create_order(self, orders_expected):
        uow = FakeUnitOfWork()
        services = WarehouseService(uow=uow)
        order = orders_expected[0]
        services.create_order(products=order.products)
        assert uow.orders.get(order_id=order.id) is not None
        assert uow.committed
        assert uow.products.list() == order.products
