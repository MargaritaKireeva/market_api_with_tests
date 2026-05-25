from fastapi import APIRouter, HTTPException

from app.repositories.users_repo import UsersRepo
from app.services.auth_service import AuthService
from app.models.schemas import RegisterRequest, LoginRequest, UserResponse, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

service = AuthService(UsersRepo())

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    summary="Register user"
)
def register(data: RegisterRequest):
    return service.register(data.email, data.password)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user"
)
def login(data: LoginRequest):
    token = service.login(data.email, data.password)

    if not token:
        raise HTTPException(401)

    return token
