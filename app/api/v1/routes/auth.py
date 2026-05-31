from fastapi import APIRouter, HTTPException

from app.api.exceptions.auth_exceptions import UserAlreadyExistsError, InvalidCredentialsError
from app.repositories.users_repo import UsersRepo
from app.services.auth_service import AuthService
from app.models.schemas import RegisterRequest, LoginRequest, UserResponse, TokenResponse, ErrorResponse

router = APIRouter(prefix="/auth", tags=["auth"])

service = AuthService(UsersRepo())


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    summary="Register user",
    responses={
        409: {
            "model": ErrorResponse,
            "description": "User already exists"
        }
    }
)
def register(data: RegisterRequest):
    try:
        return service.register(data.email, data.password)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="User already exists"
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Invalid credentials"
        }
    }
)
def login(data: LoginRequest):
    try:
        token = service.login(data.email, data.password)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    return token
