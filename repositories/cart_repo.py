import os
import json

from mappers.cart_mapper import CartMapper
from models.cart import Cart


class CartRepo:
    def __init__(self, file_path: str = 'data/carts.json') -> None:
        self.file_path = file_path

    def _load_raw(self) -> dict[str, dict]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError("Invalid carts.json structure!")

            return data

        except FileNotFoundError:
            return {}

    def _save_raw(self, carts_raw: dict[str, dict]) -> None:
        dir_name = os.path.dirname(self.file_path)

        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        temp_file = f"{self.file_path}.tmp"

        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(carts_raw, f, indent=4, ensure_ascii=False)

        os.replace(temp_file, self.file_path)

    def save(self, cart_obj: Cart) -> None:
        carts = self._load_raw()
        cart_obj_key = str(cart_obj.user_id)
        carts[cart_obj_key] = CartMapper.to_cart_raw(cart_obj)

        self._save_raw(carts)

    def get_cart_by_user_id(self, user_id: int) -> Cart | None:
        carts = self._load_raw()
        user_cart = carts.get(str(user_id))

        if not user_cart:
            return None

        return CartMapper.to_cart_model(user_cart)