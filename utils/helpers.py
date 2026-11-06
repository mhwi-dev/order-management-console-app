from models.product import Product


class Helper:

    @staticmethod
    def non_empty(message: str) -> str:

        while True:
            value = input(message).strip()

            if value:
                return value

            print("ERROR: This field cannot be empty! Try again.")

    @staticmethod
    def input_is_valid(
        message: str,
        start: int | None = 0,
        end: int | None = None
    ) -> int:
        
        while True:
            try: 
                value = int(Helper.non_empty(message))

                if start is not None and value < start:
                    print(f"ERROR: Values must be >= {start}! Try again.")
                    continue

                if end is not None and value > end:
                    print(f"ERROR: Values must be <= {end}! Try again.")
                    continue

                return value

            except ValueError:
                print("ERROR: This field must be a valid integer! Try again.")

    @staticmethod
    def input_positive(
        message: str,
        allow_zero: bool = False
    ) -> int:
        
        while True:
            try:
                value = int(Helper.non_empty(message))

                if value > 0 or (allow_zero and value == 0):
                    return value

                print(
                    "ERROR: Value must be "
                    + ("greater than or equal to 0!" if allow_zero
                       else "greater than 0!")
                )

            except ValueError:
                print("ERROR: This field must be a positive number! Try again.")

    @staticmethod
    def is_valid(
        p_id: int,
        product: Product | None,
        allow_show_stock_0: bool = False
    ) -> bool:

        if product is None:
            return False
        
        if p_id <= 0 or product.product_id != p_id:
            return False

        if not product.name or not product.name.strip():
            return False

        if product.price is None or product.price < 0:
            return False

        if product.stock is None or product.stock < 0:
            return False

        if product.stock == 0 and not allow_show_stock_0:
            return False

        if not allow_show_stock_0 and product.stock == 0:
            return False

        return True

    @staticmethod
    def input_optional_positive(
        message: str,
        is_float: bool = False
    ) -> int | float | None:
        
        while True:
            inp = input(message).strip()

            if not inp:
                return None

            try:
                value = float(inp) if is_float else int(inp)

                if value < 0:
                    print("ERROR: Value must be >= 0! Try again.")
                    continue

                return value

            except ValueError:
                print("ERROR: Invalid number! Try again.")