from fastapi import APIRouter, HTTPException, Depends

from app.api.exceptions.cart_exceptions import CartEmptyException
from app.api.exceptions.order_exceptions import OrderNotFoundException, InvalidOrderStatusError
from app.core.auth import get_current_user
from app.models.schemas import OrderResponse, StatusResponse, ErrorResponse, OrderStatus
from app.repositories.orders_repo import OrdersRepo
from app.repositories.cart_repo import CartRepo
from app.services.orders_service import OrdersService

router = APIRouter(prefix="/orders", tags=["orders"])

service = OrdersService(OrdersRepo(), CartRepo())


@router.post(
    "",
    response_model=OrderResponse,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Cart is empty"
        },
        401: {
            "model": ErrorResponse,
            "description": "Invalid or expired token"
        }
    }
)
def create_order(user_id: int = Depends(get_current_user)):
    try:
        return service.create_order(user_id)
    except CartEmptyException:
        raise HTTPException(400, "Cart is empty")


@router.get("/{order_id}",
            response_model=OrderResponse,
            responses={
                401: {
                    "model": ErrorResponse,
                    "description": "Invalid or expired token"
                },
                404: {
                    "model": ErrorResponse,
                    "description": "Order not found"
                }
            })
def get_order(order_id: int, user_id: int = Depends(get_current_user)):
    try:
        order = service.get_order(order_id)
        if order["user_id"] != user_id:
            raise OrderNotFoundException()
        return order
    except OrderNotFoundException:
        raise HTTPException(404, "Order not found")


@router.patch(
    "/{order_id}/status",
    response_model=StatusResponse,
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Invalid or expired token"
        },
        404: {
            "model": ErrorResponse,
            "description": "Order not found"
        },
        422: {
            "model": ErrorResponse,
            "description": "Invalid status"
        }
    }
)
def update_status(order_id: int, status: str, user_id: int = Depends(get_current_user)):
    try:
        order = service.get_order(order_id)
        if order["user_id"] != user_id:
            raise OrderNotFoundException()
        return service.update_status(order_id, status)
    except OrderNotFoundException:
        raise HTTPException(404, "Order not found")
    except InvalidOrderStatusError:
        raise HTTPException(422, f"Invalid status. Allowed: {[s.value for s in OrderStatus]}")


@router.post(
    "/{order_id}/cancel",
    response_model=StatusResponse,
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Invalid or expired token"
        },
        404: {
            "model": ErrorResponse,
            "description": "Order not found"
        }
    }
)
def cancel(order_id: int, user_id: int = Depends(get_current_user)):
    try:
        order = service.get_order(order_id)
        if order["user_id"] != user_id:
            raise OrderNotFoundException()
        return service.cancel(order_id)
    except OrderNotFoundException:
        raise HTTPException(404, "Order not found")
