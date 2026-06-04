import pytest

from app.core.auth import get_user_id_from_token
from app.models.schemas import RegisterRequest, LoginRequest
from app.repositories.users_repo import UsersRepo

PASSWORD_MAX_LENGTH = 30

user_repo = UsersRepo()


@pytest.mark.parametrize("email,password", [
    ("user@mail.com", "123456"),
    ("u12349@gmail.com", "1234567"),
    ("95969ODJ@yandex.ru", "1" * PASSWORD_MAX_LENGTH),
])
def test_register(email, password, base_url, http_client):
    body = RegisterRequest(email=email, password=password).model_dump()
    response = http_client.post(f"{base_url}/auth/register", json=body)
    data = response.json()
    user = user_repo.get_by_id(data["id"])

    assert response.status_code == 201
    assert data["email"] == email

    assert user["id"] == data["id"]
    assert user["email"] == email
    assert user["password"] is not None


def test_duplicate_email_register(base_url, http_client):
    body = RegisterRequest(email="user@mail.ru", password="password").model_dump()
    http_client.post(f"{base_url}/auth/register", json=body)
    response = http_client.post(f"{base_url}/auth/register", json=body)
    data = response.json()
    assert response.status_code == 409
    assert data["detail"] == "User already exists"


@pytest.mark.parametrize("email",
                         ["", "1", "mail.ru", "@mail.ru", "user@mail.ri",
                          "user@fmdd.ru", "user@mail", "^&@^8=*.&*"
                          ])
def test_invalid_email_register(base_url, http_client, email):
    response = http_client.post(
        f"{base_url}/auth/register",
        json={"email": email, "password": "password"}
    )
    data = response.json()

    assert response.status_code == 422
    assert "value is not a valid email address" in data["detail"][0]["msg"]


@pytest.mark.parametrize("password",
                         ["", "12345"])
def test_short_password(base_url, http_client, password):
    response = http_client.post(
        f"{base_url}/auth/register",
        json={"email": "user@mail.ru", "password": password}
    )
    data = response.json()

    assert response.status_code == 422
    assert "String should have at least 6 characters" in data["detail"][0]["msg"]


def test_long_password(base_url, http_client):
    password = "1" * (PASSWORD_MAX_LENGTH + 1)
    response = http_client.post(
        f"{base_url}/auth/register",
        json={"email": "user@mail.ru", "password": password}
    )
    data = response.json()

    assert response.status_code == 422
    assert "String should have at most 30 characters" in data["detail"][0]["msg"]


def test_empty_body_register(base_url, http_client):
    body = {}
    response = http_client.post(f"{base_url}/auth/register", json=body)
    data = response.json()

    assert response.status_code == 422
    assert "email" in data["detail"][0]["loc"]
    assert "password" in data["detail"][1]["loc"]
    assert "Field required" in data["detail"][0]["msg"]
    assert "Field required" in data["detail"][1]["msg"]


def test_empty_field_register(base_url, http_client):
    response = http_client.post(
        f"{base_url}/auth/register",
        data='{"email": "user@mail.com", "password": }',
        headers={"Content-Type": "application/json"}
    )
    data = response.json()

    assert response.status_code == 422
    assert "JSON decode error" in data["detail"][0]["msg"]


def test_correct_login(base_url, http_client, registered_user):
    body = LoginRequest(email=registered_user["email"],
                        password=registered_user["password"]).model_dump()
    response = http_client.post(f"{base_url}/auth/login", json=body)
    data = response.json()

    assert response.status_code == 200
    assert data["token"]
    assert get_user_id_from_token(data["token"]) == registered_user["id"]


def test_wrong_email_login(base_url, http_client, registered_user):
    email = f"wrong_{registered_user["email"]}"
    body = LoginRequest(email=email,
                        password=registered_user["password"]).model_dump()
    response = http_client.post(f"{base_url}/auth/login", json=body)
    data = response.json()

    assert response.status_code == 401
    assert data["detail"] == "Invalid credentials"


def test_wrong_password_login(base_url, http_client, registered_user):
    password = f"wrong_{registered_user["password"]}"
    body = LoginRequest(email=registered_user["email"],
                        password=password).model_dump()
    response = http_client.post(f"{base_url}/auth/login", json=body)
    data = response.json()

    assert response.status_code == 401
    assert data["detail"] == "Invalid credentials"


def test_empty_body_login(base_url, http_client):
    response = http_client.post(f"{base_url}/auth/login", json={})
    data = response.json()

    assert response.status_code == 422
    assert "email" in data["detail"][0]["loc"]
    assert "password" in data["detail"][1]["loc"]
    assert "Field required" in data["detail"][0]["msg"]
    assert "Field required" in data["detail"][1]["msg"]


def test_empty_field_login(base_url, http_client):
    response = http_client.post(
        f"{base_url}/auth/login",
        data='{"email": "user@mail.com", "password": }',
        headers={"Content-Type": "application/json"}
    )
    data = response.json()

    assert response.status_code == 422
    assert "JSON decode error" in data["detail"][0]["msg"]
