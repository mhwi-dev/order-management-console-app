from models.order import Order
from models.cart import CartItem


class OrderService:
    def __init__(self, order_repo, user_service, cart_service, product_service):
        self.order_repo = order_repo
        self.user_service = user_service
        self.cart_service = cart_service
        self.product_service = product_service

    def place_order(
        self,
        user_id: int,
        order_type: str,
        address: str,
        select_items: list[CartItem] | None = None
    ) -> Order:

        if not select_items:
            raise ValueError("ERROR: No products selected!")

        user_obj = self.user_service.get_user_by_id(user_id)

        if not user_obj:
            raise ValueError(f"ERROR: User ID #{user_id} not exists!")

        order_items = []

        for item in select_items:
            product_id = item.product.product_id

            current_product = self.product_service.get_product_by_id(product_id)

            if not current_product:
                raise ValueError(
                    f"ERROR: Product ID #{product_id} not exists!"
                )

            if item.quantity > current_product.stock:
                raise ValueError(
                    f"ERROR: Not enough stock for product #{product_id}!"
                )

            new_item = CartItem(
                product=current_product,
                quantity=item.quantity,
                note=item.note
            )

            order_items.append(new_item)

        total = sum(item.total_price() for item in order_items)

        items_dict = {
            item.product.product_id: item
            for item in order_items
        }

        next_id = self.order_repo.get_next_id()

        new_order = Order(
            order_id=next_id,
            user_id=user_obj.user_id,
            items=items_dict,
            order_type=order_type,
            address=address,
            total=total,
            status='pending'
        )

        for item in order_items:
            self.product_service.reduce(
                item.product.product_id,
                item.quantity
            )

        self.order_repo.save(new_order)

        selected_product_ids = [
            item.product.product_id
            for item in order_items
        ]

        self.cart_service.remove_items_from_cart(
            user_id,
            selected_product_ids
        )

        return new_order