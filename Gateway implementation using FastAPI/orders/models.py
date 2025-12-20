fake_order_list = [
    {"order_id": 1, "name": "Laptop", "price": 999.99},
    {"order_id": 2, "name": "Smartphone", "price": 499.99},
    {"order_id": 3, "name": "Tablet", "price": 299.99},
]

class Order:
    def __init__(self, order_id: int, name: str, price: float):

        self.order_id = order_id
        self.name = name
        self.price = price

    @classmethod
    def get_all_orders(cls):
        return [cls(**prod) for prod in fake_order_list]

    @classmethod
    def get_order_by_id(cls, order_id: int):
        product_data = next((prod for prod in fake_order_list if prod["order_id"] == order_id), None)
        if product_data:
            return cls(**product_data)
        return None

    @classmethod
    def create_order(cls, name: str, price: float):
        new_id = max(prod["id"] for prod in fake_order_list) + 1
        new_product = {"order_id": new_id, "name": name, "price": price}
        fake_order_list.append(new_product)
        return cls(**new_product)