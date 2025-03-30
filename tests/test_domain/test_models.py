class TestModels:
    def test_can_add_product_to_order(
        self, products_expected, orders_expected
    ):
        order = orders_expected[0]
        product = products_expected[2]
        order.add_product(product=product)
        assert product in order.products
