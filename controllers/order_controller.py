from utils.helpers import Helper
from models.cart import CartItem

class OrderController:
    def __init__(self, order_service, cart_service):
        self.order_service = order_service
        self.cart_service = cart_service

    def handle_place_order(self, user_id):
        user_cart = self.cart_service.get_cart_by_id(user_id)

        if not user_cart:
            return

        select_items = []
        
        while True:
            print("\n================================= PLACE ORDER ==========================")

            product_id = Helper.input_positive("Enter Product ID (ENTER 0 TO RETURN): ", allow_zero= True)

            if product_id == 0:
                print("NOTIFY: Returning menu.......")
                return
            
            if not user_cart.has_product(product_id):
                print(f"ERROR: Product ID #{product_id} not exists! Try again.")
                continue

            if any(item.product.product_id == product_id for item in select_items):
                print(f"NOTIFY: Product ID #{product_id} already in your selected!")
                continue

            cart_item = user_cart.items[product_id]
            max_qty = cart_item.quantity

            while True:
                buy_qty = Helper.input_is_valid(f"Enter quantity to order (Max {max_qty}): ")

                if buy_qty > max_qty:
                    print(f"ERROR: Quantity exceeds item in your cart! Try again.")
                    continue
                else: break

            selected = CartItem(cart_item.product, buy_qty, cart_item.note)
            select_items.append(selected)

            print('-'*60)
            print(f"NOTIFY: Added '{cart_item.product.name}' (x{buy_qty}) to order successfully!")
            print(f"\n{'-'*60}")
            choice = Helper.non_empty("Do you want to select more items? (y/n): ")

            while choice not in ['y','n']:
                print("NOTIFY: Please enter 'y' for Yes or 'n' for No! Try again.")
                choice = Helper.non_empty("Do you want to select more items? (y/n): ")

            if choice == 'n':
                print("NOTIFY: Confirm place order.... ---->")
                break

        type = Helper.non_empty("Enter type order: ")
        address = Helper.non_empty("Enter address: ")

        order = self.order_service.place_order(user_id, type, address, select_items)
        print('-'*60)
        print(f"NOTIFY: Place Order with Order ID #{order.order_id} successfully!")
        print(f"\n{'-'*60}")


            




