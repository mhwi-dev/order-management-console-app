from utils.helpers import Helper

class MainController:
    def __init__(self, user_controller, product_controller, cart_controller, order_controller):
        self.user_controller = user_controller
        self.product_controller = product_controller
        self.cart_controller = cart_controller
        self.order_controller = order_controller

    def print_menu_admin(self):
        print("\n================================== MENU ADMIN ===========================")
        message = [
            '1. SIGN UP ADMIN / CUSTOMER',
            '2. SHOW USERS INVALID',
            '3. SHOW PRODUCTS INVALID',
            '4. ADD NEW PRODUCT',
            '5. REVIEW & UPDATE PRODUCTS',
            '6. REVIEW & DELETE PRODUCTS',
            '7. LOG OUT'
        ]

        print('\n'.join(message))

        inp = Helper.input_is_valid("Enter choice: ",1, len(message))

        return inp 

    def print_menu_customer(self):
        print("\n================================== MENU CUSTOMER ===========================")
        message = [
            '1. SHOW PRODUCTS',
            '2. ADD PRODUCT TO CART',
            '3. VIEW MY CART',
            '4. PLACE ORDER',
            '5. LOG OUT'
        ]

        print('\n'.join(message))

        inp = Helper.input_is_valid("Enter choice: ",1, len(message))

        return inp 

    def run(self): 
        while True:
            print("\n================================== WELCOME TO CONSOLE APP ===========================")
            print('1. Login | 2. Sign up | 3. Exit')
            print('\n-------------------------------------------------------------------------------------')
            choice = Helper.input_is_valid("Enter chocie: ",1,3)

            if choice == 1:
                current_user = self.user_controller.handle_login()

                if current_user:
                    self.show_role_menu(current_user)

            elif choice == 2:
                self.user_controller.handle_sign_up()

            else:
                print("NOTIFY: See you again!")
                return

    def show_role_menu(self, current_user):
        while True:
            if current_user.role == 'admin':
                choice = self.print_menu_admin()

                if choice == 1:
                    self.user_controller.handle_sign_up(current_user)

                elif choice == 2:
                    self.user_controller.handle_get_users_invalid()

                elif choice == 3:
                    self.product_controller.handle_get_products_invalid()

                elif choice == 4:
                    self.product_controller.handle_add_new_product()

                elif choice == 5:
                    self.product_controller.handle_show_products()
                    self.product_controller.handle_get_products_invalid()
                    self.product_controller.handle_update_product()

                elif choice == 6:
                    self.product_controller.handle_show_products()
                    self.product_controller.handle_get_products_invalid()
                    self.product_controller.handle_delete_product()

                elif choice == 7:
                    print("Log out....")
                    return

            elif current_user.role == 'customer':
                choice = self.print_menu_customer()

                if choice == 1:
                    self.product_controller.handle_show_products_customer()

                elif choice == 2:
                    self.product_controller.handle_show_products_customer()
                    self.cart_controller.handle_add_to_cart(current_user.user_id)

                elif choice == 3:
                    self.cart_controller.handle_show_cart_details(current_user.user_id)

                elif choice == 4:
                    self.cart_controller.handle_show_cart_details(current_user.user_id)
                    self.order_controller.handle_place_order(current_user.user_id)

                elif choice == 5:
                    print("Log out....")
                    return

            else:
                print(f"\n[ERROR] Invalid user role: '{current_user.role}'")
                return