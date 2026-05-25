from fastapi import APIRouter

from app.repositories.cart_repo import CartRepo
from app.services.cart_service import CartService
from app.models.schemas import CartAdd, StatusResponse

router = APIRouter(prefix="/cart", tags=["cart"])

service = CartService(CartRepo())


@router.post(
    "/add",
    response_model=StatusResponse
)
def add(item: CartAdd):
    service.add_item(item.user_id, item.product_id, item.quantity)
    return {"status": "added"}


@router.get(
    "/{user_id}",
    response_model=list[dict]
)
def get(user_id: int):
    return service.get_cart(user_id)


@router.delete("/remove/{user_id}")
def clear(user_id: int):
    return service.clear_cart(user_id)