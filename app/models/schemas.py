from enum import Enum

from pydantic import BaseModel, Field, EmailStr


class OrderStatus(Enum):
    created = "created"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


# REQUESTS

class RegisterRequest(BaseModel):
    email: EmailStr = Field(example="user@mail.com")
    password: str = Field(min_length=6, example="secret123")


class LoginRequest(BaseModel):
    email: EmailStr = Field(example="user@mail.com")
    password: str = Field(example="secret123")


class ProductCreate(BaseModel):
    name: str = Field(example="iPhone 15")
    price: float = Field(gt=0, example=999.99)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, example="iPhone 15 Pro")
    price: float | None = Field(default=None, gt=0, example=1299.99)


class CartAdd(BaseModel):
    product_id: int = Field(example=1)
    quantity: int = Field(gt=0, example=2)


# RESPONSES

class UserResponse(BaseModel):
    id: int = Field(example=1)
    email: str = Field(example="user@mail.com")


class TokenResponse(BaseModel):
    token: str = Field(example="token-1")


class ProductResponse(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="iPhone 15")
    price: float = Field(example=999.99)


class StatusResponse(BaseModel):
    status: str = Field(example="success")


class OrderResponse(BaseModel):
    id: int = Field(example=1)
    user_id: int = Field(example=1)
    status: OrderStatus = Field(example=OrderStatus.created)


class ErrorResponse(BaseModel):
    detail: str = Field(
        example="Error message"
    )
