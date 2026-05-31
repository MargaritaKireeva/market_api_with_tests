from fastapi import APIRouter, HTTPException
from app.api.exceptions.product_exceptions import ProductNotFoundException
from app.repositories.products_repo import ProductsRepo
from app.services.products_service import ProductService
from app.models.schemas import ProductCreate, ProductUpdate, ProductResponse, StatusResponse, ErrorResponse

router = APIRouter(prefix="/products", tags=["products"])

service = ProductService(ProductsRepo())


@router.post(
    "",
    response_model=ProductResponse,
    status_code=201
)
def create(product: ProductCreate):
    return service.create(product)


@router.get("",
            response_model=list[ProductResponse],
            status_code=200)
def get_all():
    return service.get_all()


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Product not found"
        }
    }
)
def get(product_id: int):
    try:
        return service.get(product_id)
    except ProductNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


@router.patch("/{product_id}",
              response_model=ProductResponse)
def update(product_id: int, product: ProductUpdate):
    try:
        return service.update(product_id, product)
    except ProductNotFoundException:
        raise HTTPException(404, "Product not found")


@router.delete(
    "/{product_id}",
    response_model=StatusResponse
)
def delete(product_id: int):
    try:
        service.delete(product_id)
    except ProductNotFoundException:
        raise HTTPException(404, "Product not found")

    return {"status": "deleted"}
