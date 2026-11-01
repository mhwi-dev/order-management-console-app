class CartItem:
    def __init__(self, product, quantity, note):
        self.product = product
        self.quantity = quantity
        self.note = note

    def total_price(self):
        return self.product.price * self.quantity

class Cart:
    def __init__(self, user_id, items = None):
        self.user_id = user_id 
        self.items = items if items is not None else {}

    def has_product(self, product_id):
        return int(product_id) in self.items

    def add_item(self, product, quantity, note):
        product_key = int(product.product_id)

        if product_key not in self.items:
            if quantity > product.stock:
                raise ValueError(f"ERROR: Not enough stock! Product: {product.name} only {product.stock} left.")
            else:
                self.items[product_key] = CartItem(product, quantity, note)
        else:
            current_quantity = self.items[product_key].quantity
            new_quantity = current_quantity + quantity

            if new_quantity > product.stock:
                raise ValueError(f"ERROR: Not enough stock! Product: {product.name} only {product.stock} left.")
            
            self.items[product_key].quantity = new_quantity

            if note:
                self.items[product_key].note = note
        return True

    def remove_item(self, product_id: int) -> bool:
        product_key = int(product_id)

        if product_key in self.items:
            del self.items[product_key]
            return True

        return False

    def remove_items(self, products_ids: list) -> int:
        removed_count = 0

        for p_id in products_ids:
            if self.remove_item(p_id):
                removed_count += 1

        return removed_count

    def clear(self) -> None:
        self.items.clear()
    
    @property
    def calculate_total_cart(self):
        return sum(item.total_price() for item in self.items.values())
        

