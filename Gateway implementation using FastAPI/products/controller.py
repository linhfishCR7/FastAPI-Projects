from fastapi import APIRouter, Request
from models import Product
from schemas import ProductCreate


router = APIRouter()

@router.get("/products")
async def read_products(request: Request):
    products = Product.get_all_products()
    headers = dict(request.headers)
    return {
        "data": products,
        "status": "success",
        "message": "List of products"
        }


@router.post("/products")
async def create_product(product: ProductCreate):
    new_product = Product.create_product(name = product.name, price = product.price)
    return {
        "status": "success",
        "message": "Product created"
        }

@router.get("/products/{product_id}")
async def read_product(product_id: int):
    product = Product.get_product_by_id(product_id=product_id)
    return {
        "data": product,
        "status": "success",
        "message": f"Details of product {product_id}"
        }