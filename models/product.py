class Product:
    def __init__(
        self,
        product_id: int,
        name: str,
        price: float,
        stock: int
    ) -> None:
        
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self) -> str:
        return (
            f"Product ID: {self.product_id:<5} | "
            f"Name: {self.name:<20} | "
            f"Price: ${self.price:>8,.2f} | "
            f"Stock: {self.stock}"
        )

    def __repr__(self) -> str:
        return (
            f"Product(product_id={self.product_id!r}, "
            f"name={self.name!r}, "
            f"price={self.price!r}, "
            f"stock={self.stock!r})")

    def reduce_stock(self, amount: int) -> bool:
        if not isinstance(amount, int) or isinstance(amount, bool):
            return False
        
        if amount <= 0:
            return False

        if amount <= self.stock:
            self.stock -= amount
            return True

        return False    
    