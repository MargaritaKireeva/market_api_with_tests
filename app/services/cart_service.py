class CartService:

    def __init__(self, repo):
        self.repo = repo

    def add_item(self, user_id, product_id, quantity):
        return self.repo.add(user_id, product_id, quantity)

    def get_cart(self, user_id):
        return self.repo.get(user_id)

    def clear_cart(self, user_id):
        return self.repo.clear(user_id)