class OrdersService:

    def __init__(self, orders_repo, cart_repo):
        self.orders_repo = orders_repo
        self.cart_repo = cart_repo

    def create_order(self, user_id: int):
        cart_items = self.cart_repo.get(user_id)

        if not cart_items:
            return None

        order = self.orders_repo.create(user_id)

        self.cart_repo.clear(user_id)

        return order

    def get_order(self, order_id: int):
        return self.orders_repo.get(order_id)

    def update_status(self, order_id: int, status: str):
        return self.orders_repo.update_status(order_id, status)

    def cancel(self, order_id: int):
        return self.orders_repo.update_status(order_id, "cancelled")