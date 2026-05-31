from app.api.exceptions.product_exceptions import ProductNotFoundException


class ProductService:

    def __init__(self, repo):
        self.repo = repo

    def create(self, data):
        return self.repo.create(data.name, data.price)

    def get(self, product_id):
        product = self.repo.get(product_id)

        if not product:
            raise ProductNotFoundException()

        return product

    def get_all(self):
        return self.repo.get_all()

    def update(self, product_id, data):
        existing = self.repo.get(product_id)

        if not existing:
            raise ProductNotFoundException()

        name = data.name if data.name is not None else existing["name"]
        price = data.price if data.price is not None else existing["price"]

        return self.repo.update(product_id, name, price)

    def delete(self, product_id):
        existing = self.repo.get(product_id)

        if not existing:
            raise ProductNotFoundException()

        return self.repo.delete(product_id)
