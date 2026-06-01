from app.core.db_connection import get_connection
from app.api.exceptions.cart_exceptions import CartEmptyException
from app.api.exceptions.order_exceptions import OrderNotFoundException, InvalidOrderStatusError
from app.models.schemas import OrderStatus


ALLOWED_TRANSITIONS = {
    OrderStatus.created: {OrderStatus.confirmed, OrderStatus.cancelled},
    OrderStatus.confirmed: {OrderStatus.shipped, OrderStatus.cancelled},
    OrderStatus.shipped: {OrderStatus.delivered},
    OrderStatus.delivered: set(),
    OrderStatus.cancelled: set(),
}


class OrdersService:

    def __init__(self, orders_repo, cart_repo):
        self.orders_repo = orders_repo
        self.cart_repo = cart_repo

    def create_order(self, user_id: int):
        conn = get_connection()
        try:
            cart_items = self.cart_repo.get(user_id, conn=conn)

            if not cart_items:
                raise CartEmptyException()

            order = self.orders_repo.create(user_id, conn=conn)

            self.cart_repo.clear(user_id, conn=conn)

            conn.commit()
            return order
        finally:
            conn.close()

    def get_order(self, order_id: int):
        order = self.orders_repo.get(order_id)

        if not order:
            raise OrderNotFoundException()

        return order

    def update_status(self, order_id: int, status: str):
        try:
            new_status = OrderStatus(status)
        except ValueError:
            raise InvalidOrderStatusError()

        order = self.orders_repo.get(order_id)

        if not order:
            raise OrderNotFoundException()

        current_status = OrderStatus(order["status"])

        if new_status not in ALLOWED_TRANSITIONS[current_status]:
            raise InvalidOrderStatusError()

        return self.orders_repo.update_status(order_id, new_status.value)

    def cancel(self, order_id: int):
        order = self.orders_repo.get(order_id)

        if not order:
            raise OrderNotFoundException()

        current_status = OrderStatus(order["status"])

        if OrderStatus.cancelled not in ALLOWED_TRANSITIONS[current_status]:
            raise InvalidOrderStatusError()

        return self.orders_repo.update_status(order_id, "cancelled")
