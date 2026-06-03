import pytest
import requests
import os

from app.models.schemas import RegisterRequest
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


# @pytest.fixture
# def clean_users_after_test():
#     created_ids = []
#     yield created_ids
#     for user_id in created_ids:
#         user_repo.delete_by_id(user_id)


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
