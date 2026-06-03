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
    email: EmailStr = Field(json_schema_extra={"example": "user@mail.com"})
    password: str = Field(min_length=6, max_length=30, json_schema_extra={"example": "secret123"})


class LoginRequest(BaseModel):
    email: EmailStr = Field(json_schema_extra={"example": "user@mail.com"})
    password: str = Field(json_schema_extra={"example": "secret123"})


class ProductCreate(BaseModel):
    name: str = Field(json_schema_extra={"example": "iPhone 15"})
    price: float = Field(gt=0, json_schema_extra={"example": 999.99})


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, json_schema_extra={"example": "iPhone 15 Pro"})
    price: float | None = Field(default=None, gt=0, json_schema_extra={"example": 1299.99})


class CartAdd(BaseModel):
    product_id: int = Field(json_schema_extra={"example": 1})
    quantity: int = Field(gt=0, json_schema_extra={"example": 2})


# RESPONSES

class UserResponse(BaseModel):
    id: int = Field(json_schema_extra={"example": 1})
    email: str = Field(json_schema_extra={"example": "user@mail.com"})


class TokenResponse(BaseModel):
    token: str = Field(json_schema_extra={"example": "token-1"})


class ProductResponse(BaseModel):
    id: int = Field(json_schema_extra={"example": 1})
    name: str = Field(json_schema_extra={"example": "iPhone 15"})
    price: float = Field(json_schema_extra={"example": 999.99})


class StatusResponse(BaseModel):
    status: str = Field(json_schema_extra={"example": "success"})


class OrderResponse(BaseModel):
    id: int = Field(json_schema_extra={"example": 1})
    user_id: int = Field(json_schema_extra={"example": 1})
    status: OrderStatus = Field(json_schema_extra={"example": OrderStatus.created})


class ErrorResponse(BaseModel):
    detail: str = Field(
        json_schema_extra={"example": "Error message"}
    )
