from psycopg2.errors import UniqueViolation
from passlib.hash import bcrypt

from app.api.exceptions.auth_exceptions import UserAlreadyExistsError, InvalidCredentialsError


class AuthService:

    def __init__(self, repo):
        self.repo = repo

    def register(self, email: str, password: str):
        try:
            return self.repo.create(email, bcrypt.hash(password))
        except UniqueViolation:
            raise UserAlreadyExistsError()

    def login(self, email: str, password: str):
        user = self.repo.get_by_email(email)

        if not user:
            raise InvalidCredentialsError()

        if not bcrypt.verify(password, user[2]):
            raise InvalidCredentialsError()

        return {"token": f"token-{user[0]}"}
