class Order:
    def __init__(self, order_id, user, items, type, address, total, status):
        self.order_id = order_id
        self.user = user
        self.items = items
        self.type = type
        self.address = address
        self.total = total
        self.status = status

    def __str__(self):
        return (
            f"Order ID: {self.order_id:<5} | "
            f"User ID: {self.user:<5} | "
            f"Items: {self.items} | "
            f"Type: {self.type:<10} | "
            f"Address: {self.address:<15} | "
            f"Total: ${self.total:>8,.2f} | "
            f"Status: {self.status}"
        )