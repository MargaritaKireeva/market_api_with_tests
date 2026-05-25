from fastapi import APIRouter, HTTPException

from app.models.schemas import OrderResponse, StatusResponse
from app.repositories.orders_repo import OrdersRepo
from app.repositories.cart_repo import CartRepo
from app.services.orders_service import OrdersService

router = APIRouter(prefix="/orders", tags=["orders"])

service = OrdersService(OrdersRepo(), CartRepo())


@router.post(
    "",
    response_model=OrderResponse
)
def create_order(user_id: int):
    order = service.create_order(user_id)

    if not order:
        raise HTTPException(400, "Cart is empty")

    return order


@router.get("/{order_id}",
            response_model=OrderResponse)
def get_order(order_id: int):
    return service.get_order(order_id)


@router.patch(
    "/{order_id}/status",
    response_model=StatusResponse
)
def update_status(order_id: int, status: str):
    return service.update_status(order_id, status)


@router.post(
    "/{order_id}/cancel",
    response_model=StatusResponse
)
def cancel(order_id: int):
    return service.cancel(order_id)
