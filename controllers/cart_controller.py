from utils.helpers import Helper

class CartController:
    def __init__(self, cart_service, product_service):
        self.cart_service = cart_service
        self.product_service = product_service

    def handle_add_to_cart(self, user_id):
        while True:
            add_quantity = True
            print("\n============================ ADD TO CART ===========================")
            product_id = Helper.input_positive("Enter Product ID (ENTER 0 TO RETURN): ", allow_zero= True)

            if product_id == 0:
                print("NOTFY: Return menu.....")
                return

            product = self.product_service.get_product_by_id(product_id)

            if not product:
                print(f"ERROR: Product ID #{product_id} not exists! Try again.")
                continue

            if product.stock <= 0:
                print(f"ERROR: Product ID #{product_id} out of stock or not exists! Try again later.")
                continue

            while add_quantity:
                print(f"\n{'-'*60}")
                print(f"NOTIFY: Product '{product.name}' | Stock: {product.stock} left.")
                quantity = Helper.input_positive("Enter quantity (ENTER 0 TO CHANGE PRODUCT): ", allow_zero= True)

                if quantity == 0:
                    print("NOTIFY: Re-enter add to cart...")
                    add_quantity = False
                    break

                if quantity > product.stock:
                    print("ERROR: Not enough stock! Try again.")
                    continue
                break

            if not add_quantity:
                continue

            note_inp = input("Enter note (PRESS ENTER TO SKIP): ").strip()
            note = note_inp if note_inp is not None else None

            print("\n==================================================================")
            print(f"{product} | Quantity: {quantity} | Note: {note if note else 'X'}")

            print("\n------------------------------ CONFIRM STEP ------------------------")
            print('1. Cofirm, add to cart | 2. No, cancel')

            choice = Helper.input_is_valid("--> Enter choice: ",1,2)

            if choice == 2:
                print("NOTIFY: Re-enter add to cart...")
                continue

            self.cart_service.add_to_cart(user_id, product, quantity, note)
            print('-'*60)
            print(f"NOTIFY: Add Product ID #{product_id} to cart successfully!")

            print('-'*60)
            continue_add = Helper.non_empty("Do you want to add more product to cart? (y/n): ").lower()

            while continue_add not in ['y','n']:
                print("NOTIFY: Please enter 'y' for Yes or 'n' for No! Try again.")
                continue_add = Helper.non_empty("Do you want to add more product to cart? (y/n): ").lower()

            if continue_add == 'n':
                print("NOTIFY: Returning to menu...")
                return

    def handle_show_cart_details(self, user_id):
        print("\n=========================================================================================================")
        print("--------------------------------------------   MY CART   ------------------------------------------------")
        print("=========================================================================================================")

        total_cart, result = self.cart_service.show_cart_details(user_id)

        if not result:
            print("-----> NOTIFY: CART IS EMPTY! <-----")
            return

        print(f"{'ID':<5}{'Name':<15}{'Price':<16}{'Quantity':<15}{'Note':<20}{'Total Price':<15}")

        for item in result:
            price_str = f"$ {item['price']:.2f}" if item['price'] is not None else '-'
            total_str = f"$ {item['total']:.2f}" if item['total'] is not None else '-'
            note_str = f"{item['note']}" if item['note'] is not None else '-' 

            print(f"{item['product_id']:<5}{item['name']:<15}{price_str:<16}{item['quantity']:<15}{note_str:<20}{total_str:<15}")

        print(f"\n{'-'*101}")
        print(f"{'-'*35}> TOTAL AMOUNT DUE: $ {total_cart:,} <{'-'*35}")
        print('-'*101)
