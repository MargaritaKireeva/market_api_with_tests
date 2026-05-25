from fastapi import APIRouter, HTTPException
from app.repositories.products_repo import ProductsRepo
from app.services.products_service import ProductService
from app.models.schemas import ProductCreate, ProductUpdate, ProductResponse, StatusResponse

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
    product = service.get(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.patch("/{product_id}",
              response_model=ProductResponse)
def update(product_id: int, product: ProductUpdate):
    result = service.update(product_id, product)

    if not result:
        raise HTTPException(404, "Product not found")

    return result


@router.delete(
    "/{product_id}",
    response_model=StatusResponse
)
def delete(product_id: int):
    service.delete(product_id)
    return {"status": "deleted"}
