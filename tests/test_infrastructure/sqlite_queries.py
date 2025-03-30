from typing import List

from sqlalchemy import text

from sqlalchemy.orm import Session

from src.otus_hw6.domain.models import Product, Order


def insert_products(session: Session, products: List[Product]):
    sql = "INSERT INTO products(name,quantity,price) VALUES " + (
        ", ".join(
            f'("{product.name}",{product.quantity},{product.price})'
            for product in products
        )
    )
    session.execute(text(sql))


def select_all_products(session: Session) -> List[Product]:
    return [
        Product(id=t[0], name=t[1], quantity=t[2], price=t[3])
        for t in list(
            session.execute(
                text(
                    'SELECT id, name, quantity, price  FROM "products" ORDER BY id'
                )
            )
        )
    ]


def insert_orders(session: Session, orders: List[Order]):
    for order in orders:
        session.execute(text("INSERT INTO orders VALUES(NULL)"))
        insert_products(session=session, products=order.products)
        for product in order.products:
            session.execute(
                text(
                    "INSERT INTO "
                    "order_product_associations("
                    "order_id,product_id) VALUES("
                    f"{order.id},{product.id})"
                )
            )


def select_all_orders(session: Session) -> List[Order]:
    orders = list(session.execute(text('SELECT id FROM "orders" ORDER BY id')))

    ord_prods = list(
        session.execute(
            text(
                "SELECT order_id, product_id "
                'FROM "order_product_associations" ORDER BY order_id, '
                "product_id"
            )
        )
    )

    products = list(
        session.execute(
            text(
                'SELECT id, name, quantity, price  FROM "products" ORDER BY id'
            )
        )
    )

    orders_db: List[Order] = []
    for ord_id in orders:
        # Список ID продуктов
        ord_p = [
            t[1] for t in list(filter(lambda x: x[0] == ord_id[0], ord_prods))
        ]
        # Список продуктов в заказе
        prod = [
            Product(id=t[0], name=t[1], quantity=t[2], price=t[3])
            for t in list(filter(lambda x: x[0] in ord_p, products))
        ]
        # Добавляем заказ в список
        orders_db.append(Order(id=ord_id[0], products=prod))

    return orders_db


def sqlite_cleanup_db(session: Session):
    session.execute(text("DELETE FROM order_product_associations"))
    session.execute(text("DELETE FROM orders"))
    session.execute(text("DELETE FROM products"))
