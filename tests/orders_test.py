import pytest

from app.models.schemas import RegisterRequest, LoginRequest
from app.repositories.orders_repo import OrdersRepo
from app.repositories.cart_repo import CartRepo

orders_repo = OrdersRepo()
cart_repo = CartRepo()


def test_create_correct_order(base_url, http_client, auth_header, registered_user, cart_with_sample_product):
    response = http_client.post(f"{base_url}/orders", headers=auth_header)
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "created"

    order = orders_repo.get(data["id"])
    assert order is not None
    assert order["user_id"] == registered_user["id"]
    assert order["status"] == "created"

    cart = cart_repo.get(registered_user["id"])
    assert cart == []


def test_create_order_empty_cart(base_url, http_client, auth_header, registered_user):
    response = http_client.post(f"{base_url}/orders", headers=auth_header)
    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "Cart is empty"


def test_get_order(base_url, http_client, auth_header, registered_user, cart_with_sample_product):
    create_resp = http_client.post(f"{base_url}/orders", headers=auth_header)
    order_id = create_resp.json()["id"]

    response = http_client.get(f"{base_url}/orders/{order_id}", headers=auth_header)
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == order_id
    assert data["user_id"] == registered_user["id"]
    assert data["status"] == "created"


@pytest.mark.parametrize("method,url", [
    ("GET", "/orders/99999"),
    ("PATCH", "/orders/99999/status?status=confirmed"),
    ("POST", "/orders/99999/cancel"),
])
def test_orders_not_found(http_client, base_url, auth_header, method, url):
    response = http_client.request(method, f"{base_url}{url}", headers=auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_get_order_other_user(base_url, http_client, auth_header, cart_with_sample_product, second_auth_header):
    create_resp = http_client.post(f"{base_url}/orders", headers=auth_header)
    order_id = create_resp.json()["id"]

    response = http_client.get(f"{base_url}/orders/{order_id}", headers=second_auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


@pytest.mark.parametrize("method,url", [
    ("POST", "/orders"),
    ("GET", "/orders/1"),
    ("PATCH", "/orders/1/status?status=confirmed"),
    ("POST", "/orders/1/cancel"),
])
def test_orders_without_token(http_client, base_url, method, url):
    response = http_client.request(method, f"{base_url}{url}")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.parametrize("steps,target_status", [
    ([], "confirmed"),
    ([], "cancelled"),
    (["confirmed"], "shipped"),
    (["confirmed"], "cancelled"),
    (["confirmed", "shipped"], "delivered")
])
def test_update_status_valid(http_client, base_url, steps, target_status,
                             cart_with_sample_product, auth_header):
    create_resp = http_client.post(f"{base_url}/orders", headers=auth_header)
    order_id = create_resp.json()["id"]
    for step in steps:
        http_client.patch(f"{base_url}/orders/{order_id}/status",
                          params={"status": step}, headers=auth_header)

    update_resp = http_client.patch(f"{base_url}/orders/{order_id}/status",
                                    params={"status": target_status}, headers=auth_header)

    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == target_status

    order = orders_repo.get(order_id)
    assert order["status"] == target_status


@pytest.mark.parametrize("steps,target_status", [
    ([], "shipped"),
    ([], "delivered"),
    (["confirmed"], "created"),
    (["confirmed"], "delivered"),
    (["confirmed", "shipped"], "confirmed"),
    (["confirmed", "shipped"], "cancelled"),
    (["confirmed", "shipped", "delivered"], "shipped"),
    (["confirmed", "shipped", "delivered"], "delivered"),
])
def test_update_status_invalid(http_client, base_url, steps, target_status,
                                cart_with_sample_product, auth_header):
    create_resp = http_client.post(f"{base_url}/orders", headers=auth_header)
    order_id = create_resp.json()["id"]

    for step in steps:
        http_client.patch(f"{base_url}/orders/{order_id}/status",
                          params={"status": step}, headers=auth_header)

    update_resp = http_client.patch(f"{base_url}/orders/{order_id}/status",
                                    params={"status": target_status}, headers=auth_header)

    assert update_resp.status_code == 422


def test_update_status_invalid_value(http_client, base_url, cart_with_sample_product, auth_header):
    create_resp = http_client.post(f"{base_url}/orders", headers=auth_header)
    order_id = create_resp.json()["id"]

    update_resp = http_client.patch(f"{base_url}/orders/{order_id}/status",
                                    params={"status": "invalid"}, headers=auth_header)

    assert update_resp.status_code == 422


def test_cancel_order(http_client, base_url, auth_header, cart_with_sample_product):
    create_resp = http_client.post(f"{base_url}/orders", headers=auth_header)
    order_id = create_resp.json()["id"]

    cancel_resp = http_client.post(f"{base_url}/orders/{order_id}/cancel", headers=auth_header)
    assert cancel_resp.status_code == 200
    assert cancel_resp.json()["status"] == "cancelled"

    order = orders_repo.get(order_id)
    assert order["status"] == "cancelled"


def test_cancel_cancelled_order(http_client, base_url, auth_header, cart_with_sample_product):
    create_resp = http_client.post(f"{base_url}/orders", headers=auth_header)
    order_id = create_resp.json()["id"]

    http_client.post(f"{base_url}/orders/{order_id}/cancel", headers=auth_header)
    cancel_resp = http_client.post(f"{base_url}/orders/{order_id}/cancel", headers=auth_header)

    assert cancel_resp.status_code == 422
