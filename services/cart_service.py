from models.cart import Cart

class CartSerivce:
    def __init__(self, cart_repo):
        self.cart_repo = cart_repo

    def get_cart_by_id(self, user_id):
        return self.cart_repo.get_cart_by_user_id(user_id)

    def add_to_cart(self, user_id, product, quantity, note):
        user_cart = self.cart_repo.get_cart_by_user_id(user_id)

        if not user_cart:
            user_cart = Cart(user_id)

        user_cart.add_item(product, quantity, note)

        self.cart_repo.save(user_cart)

        return user_cart

    def show_cart_details(self, user_id):
        user_cart = self.cart_repo.get_cart_by_user_id(user_id)

        if not user_cart or len(user_cart.items) == 0:
            return [], 0

        total_cart = user_cart.calculate_total_cart

        result = []

        for items in user_cart.items.values():
            total = items.total_price()
            result.append({
                "product_id": items.product.product_id,
                "name": items.product.name,
                "price": items.product.price,
                "quantity": items.quantity,
                "note": items.note,
                "total": total
            })

        return total_cart, result

    def remove_items_from_cart(self, user_id: int, product_ids: list):
        user_cart = self.cart_repo.get_cart_by_user_id(user_id)

        if not user_cart:
            return None

        user_cart.remove_items(product_ids)
        
        self.cart_repo.save(user_cart)
