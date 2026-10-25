from models.product import Product
from utils.helpers import Helper

class ProductService:
    def __init__(self, product_repo):
        self.product_repo = product_repo

    # SHOW PRODUCT FOR ADMIN
    def show_products(self):
        return self.product_repo.get_all()
    
    # CHECK NAME PRODUCT EXISTS
    def check_exists_by_name(self, name):
        return self.product_repo.exists_by_name(name)

    # GETS PRODUCT
    def get_product_by_id(self, product_id):
        return self.product_repo.get_product_by_product_id(product_id)

    def get_products_invalid(self) -> dict:
        products = self.product_repo.get_all()

        return {
            p_id: p
            for p_id, p in products.items()
            if not Helper._is_valid(p_id, p)
        }

    def get_products_valid_customer(self) -> dict:
        products = self.product_repo.get_all()

        return {
            p_id: p
            for p_id, p in products.items()
            if Helper._is_valid(p_id, p)
        }

    # CRUD PRODUCT
    def add_new_product(self, name, price, stock):

        if not name.strip():
            raise ValueError("ERROR: Product name cannot be empty!")

        if self.product_repo.exists_by_name(name):
            raise ValueError("ERROR: This product name already exists!")

        if price < 0:
            raise ValueError("ERROR: Price must be >= 0!")

        if stock < 0:
            raise ValueError("ERROR: Stock must be >= 0!")
        
        next_id = self.product_repo.get_next_id()

        new_product = Product(
            product_id= next_id,
            name= name,
            price= price,
            stock= stock
        )

        self.product_repo.save(new_product)

        return new_product

    def update_product(self, product_id, name = None, price = None, stock = None):
        product = self.product_repo.get_product_by_product_id(product_id)

        if name is not None:
            product.name = name

        if price is not None:
            product.price = price

        if stock is not None:
            product.stock = stock

        self.product_repo.save(product)

    def delete_product(self, product_id):
        return self.product_repo.remove_product(product_id)

    def reduce(self, product_id, quantity):
        product = self.get_product_by_id(product_id)

        if not product:
            raise ValueError (f"ERROR: Product ID #{product_id} not exists!")

        if not product.reduce_stock(quantity):
            raise ValueError (f"ERROR: Product '{product.name}' only {product.stock} left. Not enough {quantity}!")

        self.product_repo.save(product)

        return True