from fastapi import APIRouter
from models import Order
from schema import OrderCreate


router = APIRouter()


@router.get("/order-list")
async def read_orders():

    orders = Order.get_all_orders()
    return {
        "data": orders,
        "message": "List of orders"
        }

@router.post("/orders")
async def create_order(order : OrderCreate):
    Order.create_order(name = order.name, price=order.price)
    return {"message": "Order created"}

@router.get("/orders/{order_id}")
async def read_order(order_id: int):
    order = Order.get_order_by_id(order_id=order_id)
    return {
        "data": order,
        "message": f"Details of order {order_id}"
    }


