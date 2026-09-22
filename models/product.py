class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return (
            f"Product ID: {self.product_id:<5} | "
            f"Name: {self.name:<20} | "
            f"Price: ${self.price:>8,.2f} | "
            f"Stock: {self.stock}"
        )

    def __repr__(self):
        return (
            f"Product(product_id={self.product_id!r}, "
            f"name={self.name!r}, "
            f"price={self.price!r}, "
            f"quantity={self.stock!r})")

    def reduce_stock(self, amount: int):
        if amount <= 0:
            return False

        if amount <= self.stock:
            self.stock -= amount
            return True

        return False    
    