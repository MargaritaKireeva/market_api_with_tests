import pytest

from app.repositories.products_repo import ProductsRepo

products_repo = ProductsRepo()


@pytest.mark.parametrize("name,price", [
    ("русское название", 100.0),
    ("english name", 100.0),
    ("name", 1.0),
    ("a", 100.0),
    ("name", 0.01),
    ("name", 99999999.99),
])
def test_add_correct_product(http_client, base_url, name, price):
    response = http_client.post(
        f"{base_url}/products",
        json={"name": name, "price": price}
    )
    data = response.json()
    assert response.status_code == 201
    assert data["name"] == name
    assert data["price"] == price

    product = products_repo.get(data["id"])
    assert product["name"] == name
    assert product["price"] == price


@pytest.mark.parametrize("name", ["", "  "])
def test_add_product_empty_name(base_url, http_client, name):
    response = http_client.post(
        f"{base_url}/products",
        json={"name": name, "price": 100.0}
    )
    assert response.status_code == 422


def test_add_product_empty_body(base_url, http_client):
    response = http_client.post(f"{base_url}/products", json={})
    data = response.json()
    assert response.status_code == 422
    assert "name" in data["detail"][0]["loc"]
    assert "price" in data["detail"][1]["loc"]
    assert "Field required" in data["detail"][0]["msg"]
    assert "Field required" in data["detail"][1]["msg"]


def test_empty_field_add_product(base_url, http_client):
    response = http_client.post(
        f"{base_url}/products",
        data='{"name": "name", "price": }',
        headers={"Content-Type": "application/json"}
    )
    data = response.json()

    assert response.status_code == 422
    assert "JSON decode error" in data["detail"][0]["msg"]


@pytest.mark.parametrize("price", [0, -0.01, -1])
def test_add_product_invalid_price(base_url, http_client, price):
    response = http_client.post(
        f"{base_url}/products",
        json={"name": "test", "price": price}
    )
    assert response.status_code == 422


def test_get_all_products(http_client, base_url, sample_product):
    response = http_client.get(f"{base_url}/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_product_by_id(http_client, base_url, sample_product):
    product_id = sample_product["id"]
    response = http_client.get(f"{base_url}/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == sample_product["name"]
    assert data["price"] == sample_product["price"]


def test_get_product_not_found(http_client, base_url):
    response = http_client.get(f"{base_url}/products/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_delete_product(http_client, base_url, sample_product):
    delete_resp = http_client.delete(f"{base_url}/products/{sample_product["id"]}")
    assert delete_resp.status_code == 200

    get_resp = http_client.get(f"{base_url}/products/{sample_product["id"]}")
    assert get_resp.status_code == 404


def test_delete_product_not_found(http_client, base_url):
    response = http_client.delete(f"{base_url}/products/9999999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


@pytest.mark.parametrize("update_data,expected_name,expected_price", [
    ({"name": "Updated Name"}, "Updated Name", 100.0),
    ({"price": 250.0}, "Test Product", 250.0),
    ({"name": "New", "price": 500.0}, "New", 500.0),
])
def test_update_product(http_client, base_url, sample_product, update_data, expected_name, expected_price):
    response = http_client.patch(
        f"{base_url}/products/{sample_product["id"]}",
        json=update_data
    )
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == expected_name
    assert data["price"] == expected_price


def test_update_product_not_found(http_client, base_url):
    response = http_client.patch(
        f"{base_url}/products/99999",
        json={"name": "test"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_update_product_empty_body(http_client, base_url, sample_product):
    product_id = sample_product["id"]
    response = http_client.patch(
        f"{base_url}/products/{product_id}",
        json={}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == sample_product["name"]
    assert data["price"] == sample_product["price"]


@pytest.mark.parametrize("price", [0, -0.01, -1])
def test_update_product_invalid_price(http_client, base_url, sample_product, price):
    response = http_client.patch(
        f"{base_url}/products/{sample_product["id"]}",
        json={"price": price}
    )
    assert response.status_code == 422
