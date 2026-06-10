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


def test_add_to_cart_with_invalid_token(http_client, base_url, sample_product):
    response = http_client.post(
        f"{base_url}/cart/add",
        json={"product_id": sample_product["id"], "quantity": 2},
        headers={"Authorization": f"Bearer user-{id}"})
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"


def test_add_to_cart_without_token(http_client, base_url, sample_product):
    response = http_client.post(
        f"{base_url}/cart/add",
        json={"product_id": sample_product["id"], "quantity": 2})
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"


def test_add_not_found_product_to_cart(http_client, base_url, auth_header,
                                       registered_user):
    response = http_client.post(
        f"{base_url}/cart/add",
        json={"product_id": 99999, "quantity": 2},
        headers=auth_header
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Product not found"


def test_get_cart(http_client, base_url, auth_header, sample_product):
    http_client.post(
        f"{base_url}/cart/add",
        json={"product_id": sample_product["id"], "quantity": 1},
        headers=auth_header
    )
    response = http_client.get(f"{base_url}/cart", headers=auth_header)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_empty_cart(http_client, base_url, auth_header):
    response = http_client.get(f"{base_url}/cart", headers=auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Cart is empty"


def test_get_cart_with_invalid_cart(http_client, base_url, sample_product, auth_header):
    http_client.post(
        f"{base_url}/cart/add",
        json={"product_id": sample_product["id"], "quantity": 1},
        headers=auth_header
    )
    response = http_client.get(f"{base_url}/cart",
                               headers={"Authorization": f"Bearer user-{id}"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_add_invalid_quantity(http_client, base_url, auth_header, sample_product):
    response = http_client.post(
        f"{base_url}/cart/add",
        json={"product_id": sample_product["id"], "quantity": -1},
        headers=auth_header
    )
    data = response.json()
    assert response.status_code == 422
    assert "greater than 0" in data["detail"][0]["msg"]


def test_add_missing_fields(http_client, base_url, auth_header):
    response = http_client.post(
        f"{base_url}/cart/add",
        json={},
        headers=auth_header
    )
    data = response.json()
    assert response.status_code == 422
    assert "Field required" in data["detail"][0]["msg"]


def test_clear_cart(http_client, base_url, auth_header, sample_product):
    http_client.post(
        f"{base_url}/cart/add",
        json={"product_id": sample_product["id"], "quantity": 1},
        headers=auth_header
    )

    delete_resp = http_client.delete(f"{base_url}/cart/remove", headers=auth_header)
    assert delete_resp.status_code == 200

    get_resp = http_client.get(f"{base_url}/cart", headers=auth_header)
    assert get_resp.status_code == 404