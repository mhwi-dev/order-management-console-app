class Helper:

    @staticmethod
    def non_empty(message):
        while True:
            inp = input(message).strip()

            if inp == '':
                print("ERROR: This field cannot be empty! Try again.")
                continue

            return inp

    @staticmethod
    def input_is_valid(message, start = 0, end = None):
        while True:
            inp = Helper.non_empty(message)
            try:
                value = int(inp)

                if start is not None and value < start:
                    print(f"ERROR: Values must be >= {start}! Try again.")
                    continue

                if end is not None and value > end:
                    print(f"ERROR: Values must be <= {end}! Try again.")
                    continue

                return value

            except ValueError:
                print("ERROR: This field must be enter a valid interger! Try again.")

    @staticmethod
    def input_positive(message, allow_zero = False):
        while True:
            inp = Helper.non_empty(message)

            try: 
                value = int(inp)

                if (allow_zero and value >= 0) or (not allow_zero and value > 0):
                    return value

                if allow_zero:
                    print("ERROR: Value must be enter a number greater than or equal to 0! Try again.")
                else:
                    print("ERROR: Value must be enter a number greater than 0! Try again.")

            except ValueError:
                print("ERROR: This field must be enter a positive number! Try again.")

    @staticmethod
    def _is_valid(p_id, p, allow_show_stock_0 = False) -> bool:
        if not p_id or not p or not p.product_id or not p.name:
            return False

        if p.price is None or p.price < 0:
            return False

        if allow_show_stock_0:
            if p.stock is None or p.stock < 0:
                return False

        if not allow_show_stock_0:
            if p.stock is None or p.stock <= 0:
                return False

        return True

    @staticmethod
    def input_optional_positive(message, is_float = False):
        while True:
            inp = input(message).strip()

            if not inp:
                return None

            try:
                val = float(inp) if is_float else int(inp)

                if val >= 0:
                    return val

                print("ERROR: Value must be >= 0! Try again.")

            except ValueError:
                print("ERROR: Invalid number! Try again")