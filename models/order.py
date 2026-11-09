from models.cart import CartItem


class Order:
    def __init__(
        self,
        order_id: int,
        user_id: int,
        items: dict[str, CartItem],
        order_type: str,
        address: str,
        total: int,
        status: str
    ) -> None:
        self.order_id = order_id
        self.user_id = user_id
        self.items = items
        self.order_type = order_type
        self.address = address
        self.total = total
        self.status = status

    def __str__(self) -> str:
        return (
            f"Order ID: {self.order_id:<5} | "
            f"User ID: {self.user_id:<5} | "
            f"Items: {self.items} | "
            f"Order Type: {self.order_type:<10} | "
            f"Address: {self.address:<15} | "
            f"Total: ${self.total:>8,.2f} | "
            f"Status: {self.status}"
        )