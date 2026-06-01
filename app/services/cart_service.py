from app.api.exceptions.cart_exceptions import CartEmptyException
from app.api.exceptions.product_exceptions import ProductNotFoundException


class CartService:

    def __init__(self, repo, products_repo):
        self.repo = repo
        self.products_repo = products_repo

    def add_item(self, user_id, product_id, quantity):
        product = self.products_repo.get(product_id)
        if not product:
            raise ProductNotFoundException()
        return self.repo.add(user_id, product_id, quantity)

    def get_cart(self, user_id):
        items = self.repo.get(user_id)

        if not items:
            raise CartEmptyException()

        return items

    def clear_cart(self, user_id):
        return self.repo.clear(user_id)