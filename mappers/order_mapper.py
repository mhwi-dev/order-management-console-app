from mappers.cart_mapper import CartMapper
from models.users import User
from models.orders import Order

class OrderMapper:

    @staticmethod
    def to_order_model(user_obj: User, order_raw: dict) -> Order:
        if not order_raw or not isinstance(order_raw, dict):
            return None

        items_raw = order_raw.get('items', {})
        items_obj = {
            int(p_id): CartMapper.to_cart_item_model(int(p_id), item)
            for p_id, item in items_raw.items()
        }

        return Order(
            order_id= order_raw.get('order_id'),
            user= user_obj,
            items= items_obj,
            type= order_raw.get('type'),
            address= order_raw.get('address'),
            total= order_raw.get('total'),
            status= order_raw.get('status')
        )

    @staticmethod
    def to_order_raw(order_obj: Order) -> dict:
        if not order_obj or not isinstance(order_obj, Order):
            return None
        
        return {
            'order_id': order_obj.order_id,
            'user_id': order_obj.user.user_id,
            'items': {
                str(p_id): CartMapper.to_cart_item_raw(item)
                for p_id, item in order_obj.items.items()
            },
            'type': order_obj.type,
            'address': order_obj.address,
            'total': order_obj.total,
            'status': order_obj.status
        }