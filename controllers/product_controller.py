from utils.helpers import Helper

class ProductController:
    def __init__(self, product_service):
        self.product_service = product_service

    #============================================================================================
    #----------------------------- HANDLE SHOW PRODUCTS ADMIN / CUSTOMER ------------------------
    #============================================================================================
    def handle_show_products(self): # FOR ADMIN (SHOW ALL)
        products = self.product_service.show_products()

        if not products:
            print("NOTIFY: The menu haven't product yet!")
            return

        for p in products.values():
            print(p)

    def handle_show_products_customer(self): # FOR CUSTOMER (SHOW VALID AND NOT ALLOW_STOCK_0)
        print("\n================================= MENU PRODUCT ==============================")
        products = self.product_service.get_products_valid_customer()

        if not products:
            print("NOTIFY: The menu haven't product yet!")
            return

        for p in products.values():
            print(p)

    def handle_get_products_invalid(self): # FOR ADMIN (SHOW INVALID)
        print("\n================================== PRODUCT INVALID ===========================")
        products = self.product_service.get_products_invalid()

        if not products:
            print("NOTIFY: No product invalid!")
            return

        print(products)

    #============================================================================================
    #--------------------------------------- HANDLE CRUD ----------------------------------------
    #============================================================================================
    def handle_add_new_product(self):
        while True:
            print("\n============================= ADD NEW PRODUCT ===========================")
            name = Helper.non_empty("Enter product name (ENTER 0 TO RETURN): ").title()

            if name == '0':
                print("NOTIFY: Return....")
                return

            if self.product_service.check_exists_by_name(name):
                print(f"NOTIFY: Name: '{name}' already exists! Try again.")
                continue

            price = Helper.input_positive("Enter price: ", allow_zero= True)
            stock = Helper.input_positive("Enter stock: ", allow_zero= True)

            print("\n============================= REVIEW =========================")
            print(f"Name: {name} | Price: ${price:>8,.2f} | Stock: {stock}")
            print("\n---------------------------- CONFIRM STEP -------------------")
            print("1. Yes, add product | 2. No, canel")
            choice = Helper.input_is_valid("--> Enter choice: ",1,2)

            if choice == 2:
                print("NOTIFY: Cancelled adding product. Please re-enter....")
                continue

            if choice == 1:
                self.product_service.add_new_product(name, price, stock)
                print(f"\n{'-'*60}")
                print(f"NOTIFY: Add #{name} to menu successfully!")
                print(f"\n{'-'*60}")

            continue_add = Helper.non_empty("Do you want to add more product? (y/n): ").lower()

            while continue_add not in ['y','n']:
                print("ERROR: Invalid input! Please enter 'y' for Yes or 'n' for No.")
                continue_add = Helper.non_empty("Do you want to add more product? (y/n): ").lower()

            if continue_add == 'n':
                print("NOTIFY: Return....")
                return

    def handle_update_product(self):
        while True:
            print("\n============================== UPDATE PRODUCT ============================")
            product_id = Helper.input_positive("Enter Product ID (ENTER 0 TO RETURN): ", allow_zero= True)

            if product_id == 0:
                print("NOTIFY: Return.....")
                return

            product = self.product_service.get_product_by_id(product_id)

            if not product:
                print(f"ERROR: ID #{product_id} not existed! Try again")
                continue

            while True:
                name_inp = input("Enter name (ENTER TO SKIP): ").strip()
                name = name_inp.lower() if name_inp else None

                if name and name.lower() != product.name.lower() and self.product_service.check_exists_by_name(name):
                    print(f"ERROR: Name #{name} already exists! Try again.")
                    continue

                break

            price = Helper.input_optional_positive("Enter price (ENTER TO SKIP): ", is_float= True)
            stock = Helper.input_optional_positive("Enter stock (ENTER TO SKIP): ")

            print("\n------------------------------ REVIEW ---------------------------")
            print(f"Name: {product.name} ----> New name: {name if name else 'Unchanged'}")
            print(f"Price: ${product.price} ----> New price: {price if price is not None else 'Unchanged'}")
            print(f"Stock: {product.stock} ----> New stock: {stock if stock is not None else 'Unchanged'}")

            print("\n--------------------------- CONFIRM STEP ----------------------")
            print("1. Yes, Confirm | 2. Cancel")
            choice = Helper.input_is_valid("--> Enter choice: ",1,2)

            if choice == 2:
                print("NOTIFY: Cancel updating! Please re-enter update.....")
                continue

            self.product_service.update_product(product_id, name, price, stock)
            print(f"\n{'-'*60}")
            print(f"NOTIFY: Updated Product ID#{product_id} successfully!")
            print(f"\n{'-'*60}")

            continue_add = Helper.non_empty("Do you want to update more product? (y/n): ").lower()

            while continue_add not in ['y', 'n']:
                print("ERROR: Invalid input! Please enter 'y' for Yes or 'n' for No.")
                continue_add = Helper.non_empty("Do you want to update more product? (y/n): ").lower()

            if continue_add == 'n':
                print("NOTIFY: Return.....")
                return

    def handle_delete_product(self):
        while True:
            print("\n============================== DELETE PRODUCT ============================")
            product_id = Helper.input_positive("Enter Product ID (ENTER 0 TO RETURN): ")

            if product_id == 0:
                print("NOTIFY: Return....")
                return

            product = self.product_service.get_product_by_id(product_id)

            if not product:
                print(f"ERROR: ID #{product_id} not existed! Try again")
                continue

            print("\n============================== Product Information ============================")
            print(product)

            print("\n================================= CONFIRM STEP ================================")
            print('1. Confirm, delete | 2. No, cancel')

            print("\n===============================================================================")
            choice = Helper.input_is_valid("Enter choice: ",1,2)

            if choice == 2:
                print("NOTIFY: Cancel updating! Please re-enter delete.....")
                continue

            self.product_service.delete_product(product_id)
            print(f"\n{'-'*60}")
            print(f"NOTIFY: Deleted Product ID#{product_id} successfully!")
            print(f"\n{'-'*60}")

            continue_add = Helper.non_empty("Do you want to delete more product? (y/n): ").lower()

            while continue_add not in ['y', 'n']:
                print("ERROR: Invalid input! Please enter 'y' for Yes or 'n' for No.")
                continue_add = Helper.non_empty("Do you want to delete more product? (y/n): ").lower()

            if continue_add == 'n':
                print("NOTIFY: Return.....")
                return


