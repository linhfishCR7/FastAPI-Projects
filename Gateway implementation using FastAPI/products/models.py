fake_products_list = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Smartphone", "price": 499.99},
    {"id": 3, "name": "Tablet", "price": 299.99},
]

class Product:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price

    @classmethod
    def get_all_products(cls):
        return [cls(**prod) for prod in fake_products_list]

    @classmethod
    def get_product_by_id(cls, product_id: int):
        product_data = next((prod for prod in fake_products_list if prod["id"] == product_id), None)
        if product_data:
            return cls(**product_data)
        return None

    @classmethod
    def create_product(cls, name: str, price: float):
        new_id = max(prod["id"] for prod in fake_products_list) + 1
        new_product = {"id": new_id, "name": name, "price": price}
        fake_products_list.append(new_product)
        return cls(**new_product)