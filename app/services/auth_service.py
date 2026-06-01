from passlib.hash import bcrypt
import psycopg2

from app.api.exceptions.auth_exceptions import UserAlreadyExistsError, InvalidCredentialsError
from app.core.auth import create_token


class AuthService:

    def __init__(self, repo):
        self.repo = repo

    def register(self, email: str, password: str):
        try:
            return self.repo.create(email, bcrypt.hash(password))
        except psycopg2.errors.UniqueViolation:
            raise UserAlreadyExistsError()

    def login(self, email: str, password: str):
        user = self.repo.get_by_email(email)

        if not user:
            raise InvalidCredentialsError()

        if not bcrypt.verify(password, user["password"]):
            raise InvalidCredentialsError()

        return {"token": create_token(user['id'])}
