from app.api.exceptions.cart_exceptions import CartEmptyException
from app.api.exceptions.order_exceptions import OrderNotFoundException, InvalidOrderStatusError
from app.models.schemas import OrderStatus


class OrdersService:

    def __init__(self, orders_repo, cart_repo):
        self.orders_repo = orders_repo
        self.cart_repo = cart_repo

    def create_order(self, user_id: int):
        cart_items = self.cart_repo.get(user_id)

        if not cart_items:
            raise CartEmptyException()

        order = self.orders_repo.create(user_id)

        self.cart_repo.clear(user_id)

        return order

    def get_order(self, order_id: int):
        order = self.orders_repo.get(order_id)

        if not order:
            raise OrderNotFoundException()

        return order

    def update_status(self, order_id: int, status: str):
        try:
            parsed = OrderStatus(status)
        except ValueError:
            raise InvalidOrderStatusError()

        order = self.orders_repo.get(order_id)

        if not order:
            raise OrderNotFoundException()

        return self.orders_repo.update_status(order_id, parsed.value)

    def cancel(self, order_id: int):
        order = self.orders_repo.get(order_id)

        if not order:
            raise OrderNotFoundException()

        return self.orders_repo.update_status(order_id, "cancelled")