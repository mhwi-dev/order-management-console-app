from utils.helpers import Helper

class UserController:
    def __init__(self, user_service):
        self.user_service = user_service

    def handle_sign_up(self, current_user = None):
        while True:
            print("\n================================ SIGN UP =========================")
            username = Helper.non_empty("Enter username (ENTER 0 TO RETURN): ")

            if username == '0':
                print("Return....")
                return

            password = Helper.non_empty("Enter password: ")

            full_name = Helper.non_empty("Enter full name: ").title()

            target_role = 'customer'
        
            if current_user and current_user.role == 'admin':
                print("\n----------------------------- SIGN UP FOR CUSTOMER / ADMIN --------------------") 
                print("1. Sign up admin | 2. Sign up customer")
                choice = Helper.input_is_valid("--> Enter choice: ",1,2)

                target_role = 'admin' if choice == 1 else 'customer'

            print("\n-----------------------------------------------------------------------")
                            
            print(f"Username: {username} | Password: ********** | Full name: {full_name} | Role: {target_role}")

            print('\n---------------------------------- CONFIRM STEP ---------------------------')
            print("1. Yes, confirm | 2. No, cancel")
            confirm_choice = Helper.input_is_valid("--> Enter choice: ",1,2)

            if confirm_choice == 1:
                try: 
                    self.user_service.sign_up(username, password, full_name, target_role)
                    print('-'*60)
                    print(f"NOTIFY: Sign up '{full_name}' successfully!")
                    return

                except ValueError as e:
                    print(f"\n[ERROR] {e}")

            else:
                print("Sign up canceled. Please re-enter your information...")
                continue

    def handle_login(self):
        while True:
            print("\n============================ LOGIN ===========================")
            username = Helper.non_empty("Enter username (ENTER 0 TO RETURN): ")

            if username == '0':
                print("Return...")
                return

            password = Helper.non_empty("Enter password: ")

            try:
                user = self.user_service.login(username, password)
                display_name = user.full_name if user.full_name else user.username
                print('-'*60)
                print(f"Welcome back {display_name} to app! Have a nice day.")
                return user

            except ValueError as e:
                print(f"\n[ERROR] {e}")

    def handle_get_users_invalid(self):
        print("\n=========================== USERS LIST =========================")
        result = self.user_service.get_user_invalid()

        if not result:
            print("NOTIFY: All users valid!")
            return

        print(f"DEBUG USERS: {result}")