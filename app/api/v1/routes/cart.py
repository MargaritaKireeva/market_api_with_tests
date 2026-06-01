from fastapi import APIRouter, HTTPException, Depends

from app.api.exceptions.cart_exceptions import CartEmptyException
from app.api.exceptions.product_exceptions import ProductNotFoundException
from app.core.auth import get_current_user
from app.repositories.cart_repo import CartRepo
from app.repositories.products_repo import ProductsRepo
from app.services.cart_service import CartService
from app.models.schemas import CartAdd, StatusResponse, ErrorResponse

router = APIRouter(prefix="/cart", tags=["cart"])

service = CartService(CartRepo(), ProductsRepo())


@router.post(
    "/add",
    response_model=StatusResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Product not found"
        }
    }
)
def add(item: CartAdd, user_id: int = Depends(get_current_user)):
    try:
        service.add_item(user_id, item.product_id, item.quantity)
    except ProductNotFoundException:
        raise HTTPException(404, "Product not found")
    return {"status": "added"}


@router.get(
    "",
    response_model=list[dict],
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Cart is empty"
        }
    }
)
def get(user_id: int = Depends(get_current_user)):
    try:
        return service.get_cart(user_id)
    except CartEmptyException:
        raise HTTPException(
            status_code=404,
            detail="Cart is empty"
        )


@router.delete("/remove")
def clear(user_id: int = Depends(get_current_user)):
    return service.clear_cart(user_id)
