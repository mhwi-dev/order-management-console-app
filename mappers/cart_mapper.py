from models.cart import Cart, CartItem
from mappers.product_mapper import ProductMapper

class CartMapper:

    @staticmethod
    def to_cart_item_model(product_id, cart_item: dict, ) -> CartItem:
        if not cart_item or not isinstance(cart_item, dict):
            cart_item = {}

        product_raw = {
            'product_id': product_id,
            'name': cart_item.get('name'),
            'price': cart_item.get('price'),
            'stock': cart_item.get('stock', 0)
        }

        product_obj = ProductMapper.to_product_model(product_raw)

        return CartItem(
            product= product_obj,
            quantity= cart_item.get('quantity',1),
            note= cart_item.get('note')
        )

    @staticmethod
    def to_cart_item_raw(cart_item: CartItem) -> dict:
        if not cart_item or not isinstance(cart_item, CartItem):
            return None
        
        return {
            "product_id": cart_item.product.product_id,
            "name": cart_item.product.name,
            "price": cart_item.product.price,
            "quantity": cart_item.quantity,
            "note": cart_item.note
        }

    @staticmethod
    def to_cart_model(cart: dict) -> Cart:
        if not cart or not isinstance(cart, dict):
            return None
        
        items_raw = cart.get('items', {})
        items_obj = {
            int(product_id): CartMapper.to_cart_item_model(int(product_id), item)
            for product_id, item in items_raw.items()
        }

        return Cart(
            user_id= cart.get('user_id'),
            items= items_obj
        )

    @staticmethod
    def to_cart_raw(cart: Cart) -> dict:
        if not cart or not isinstance(cart, Cart):
            return None
        return {
            "user_id": cart.user_id,
            "items" : {
                str(product_id): CartMapper.to_cart_item_raw(item)
                for product_id, item in cart.items.items()
            },
        }