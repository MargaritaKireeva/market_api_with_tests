from fastapi import APIRouter, HTTPException

from app.api.exceptions.cart_exceptions import CartEmptyException
from app.repositories.cart_repo import CartRepo
from app.services.cart_service import CartService
from app.models.schemas import CartAdd, StatusResponse, ErrorResponse

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
    response_model=list[dict],
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Cart is empty"
        }
    }
)
def get(user_id: int):
    try:
        return service.get_cart(user_id)
    except CartEmptyException:
        raise HTTPException(
            status_code=404,
            detail="Cart is empty"
        )


@router.delete("/remove/{user_id}")
def clear(user_id: int):
    return service.clear_cart(user_id)