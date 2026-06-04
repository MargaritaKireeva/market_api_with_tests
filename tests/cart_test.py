from app.repositories.cart_repo import CartRepo

cart_repo = CartRepo()


def test_add_to_cart(http_client, base_url, auth_header,
                     sample_product, registered_user):
    response = http_client.post(
        f"{base_url}/cart/add",
        json={"product_id": sample_product["id"], "quantity": 2},
        headers=auth_header
    )
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "added"

    cart = cart_repo.get(registered_user["id"])
    assert len(cart) == 1
    assert cart[0]["product_id"] == sample_product["id"]
    assert cart[0]["quantity"] == 2
