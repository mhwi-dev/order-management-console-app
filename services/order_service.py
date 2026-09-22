from models.orders import Order

class OrderService:
    def __init__(self, order_repo, user_service, cart_service, product_service):
        self.order_repo = order_repo
        self.user_service = user_service
        self.cart_service = cart_service
        self.product_service = product_service

    def place_order(self, user_id, type, address, select_items: list = None):
        if select_items is None:
            return 
        
        user_obj = self.user_service.get_user_by_id(user_id)
        next_id = self.order_repo.get_next_id()
        total = sum(item.total_price() for item in select_items)
        items_dict = {
            item.product.product_id: item 
            for item in select_items
            }

        new_order = Order(
            order_id= next_id,
            user= user_obj,
            items= items_dict,
            type= type,
            address= address,
            total= total,
            status= 'pending'
        )

        self.order_repo.save(new_order)

        for item in select_items:
            self.product_service.reduce(item.product.product_id, item.quantity)

        selected_product_ids = [item.product.product_id for item in select_items]

        self.cart_service.remove_items_from_cart(user_id, selected_product_ids)
        
        return new_order