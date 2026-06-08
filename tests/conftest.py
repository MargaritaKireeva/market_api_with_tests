import pytest
import requests
import os

from app.models.schemas import RegisterRequest, LoginRequest
from app.repositories.users_repo import UsersRepo

user_repo = UsersRepo()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def http_client():
    with requests.Session() as session:
        yield session


@pytest.fixture(autouse=True, scope="function")
def clean_users_orders_carts():
    user_repo.delete_all()


@pytest.fixture
def registered_user(http_client, base_url):
    email = "user@mail.ru"
    password = "password"
    body = RegisterRequest(email=email, password=password).model_dump()
    response = http_client.post(f"{base_url}/auth/register", json=body)
    data = response.json()
    data["password"] = password
    return data


@pytest.fixture
def auth_header(http_client, base_url, registered_user):
    body = LoginRequest(
        email=registered_user["email"],
        password=registered_user["password"]
    ).model_dump()
    response = http_client.post(f"{base_url}/auth/login", json=body)
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_product(http_client, base_url):
    response = http_client.post(
        f"{base_url}/products",
        json={"name": "Test Product", "price": 100.0}
    )
    return response.json()


@pytest.fixture
def cart_with_sample_product(base_url, http_client, sample_product, auth_header):
    http_client.post(
        f"{base_url}/cart/add",
        json={"product_id": sample_product["id"], "quantity": 2},
        headers=auth_header
    )


@pytest.fixture
def second_auth_header(http_client, base_url):
    http_client.post(
        f"{base_url}/auth/register",
        json=RegisterRequest(email="user2@mail.ru", password="password").model_dump()
    )
    response = http_client.post(
        f"{base_url}/auth/login",
        json=LoginRequest(email="user2@mail.ru", password="password").model_dump()
    )
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}